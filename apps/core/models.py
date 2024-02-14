from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=765, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    whatsapp_phone = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="Telefono WhatsApp (+54)"
    )
    last_name = models.CharField(
        max_length=100,
        null=True,
    )
    first_name = models.CharField(
        max_length=100,
        null=True,
    )
    
    @property
    def full_name(self):
        return u"{} {}".format(self.first_name if self.first_name else '',
                               self.last_name if self.last_name else '')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = UserManager()

    class Meta:
        app_label = 'core'
        verbose_name = _('RapiHogar User')
        verbose_name_plural = _('RapiHogar Users')  


class Scheme(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'core'
        verbose_name = _('Esquema de un pedido')
        verbose_name_plural = _('Esquemas de pedidos')
    
    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=80)
    website = models.CharField(max_length=100)

    class Meta:
        app_label = 'core'
        verbose_name = _('Empresa')
        verbose_name_plural = _('Empresas')
    
    def __str__(self):
        return self.name


class Tecnico(models.Model):
    apellido = models.CharField(max_length=50)
    nombre = models.CharField(max_length=80)
    
    def get_hours_worked(self):
        value = self.pedidos.all().aggregate(Sum('hours_worked'))
        return value.get('hours_worked__sum', 0)
    
    @property
    def hours_worked(self):
        return self.get_hours_worked() or 0
        
    @property
    def total_pedidos(self):
        return self.pedidos.count()
    
    @property
    def full_name(self):
        return f"{self.apellido}, {self.nombre}"
    
    @property
    def total_payment(self):
        
        if self.hours_worked == 0:
            return 0
    
        # rangos y tarifas correspondientes
        pay_rates = [
            (15, 200, 0.85),
            (29, 250, 0.84),
            (48, 300, 0.83)
        ]
        default_rate = (350, 0.82)
        
        # Calcular el salario según las tarifas definidas
        for limit, rate, discount in pay_rates:
            if self.hours_worked < limit:
                return self.hours_worked * rate * discount
        
        # Si las horas trabajadas superan todos los límites definidos
        return self.hours_worked * default_rate[0] * default_rate[1]
    
    class Meta:
        verbose_name_plural = 'Técnico'
        ordering = ('apellido', 'nombre')
    
    def __str__(self):
        return self.full_name


class Pedido(models.Model):
    SOLICITUD = 0
    PEDIDO = 1

    TIPO_PEDIDO = (
        (SOLICITUD, 'Solicitud'),
        (PEDIDO, 'Pedido'),
    )
    type_request = models.IntegerField(
        choices=TIPO_PEDIDO,
        db_index=True,
        default=PEDIDO
    )
    client = models.ForeignKey(
        User,
        verbose_name='cliente',
        on_delete=models.CASCADE
    )
    scheme = models.ForeignKey(
        Scheme,
        null=True,
        on_delete=models.CASCADE
    )
    hours_worked = models.IntegerField(default=0)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name="pedidos")

    class Meta:
        app_label = 'core'
        verbose_name_plural = 'pedidos'
        ordering = ('-id', )

    def __str__(self):
        return f"{self.get_type_request_display()} | {self.client.full_name} | {self.tecnico.full_name}"
