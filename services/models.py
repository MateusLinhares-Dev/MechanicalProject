from django.db import models
from vehicles.models import Vehicle
from products.models import Product
from django.utils import timezone

class ServiceType(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Tipo de Serviço'
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição',
    )
    
    estimated_time = models.IntegerField(
        verbose_name='Tempo Estimado (minutos)',
        default=60
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço Base',
        default=0
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        verbose_name = 'Tipo de Serviço'
        verbose_name_plural = 'Tipos de Serviços'
        
    def __str__(self):
        return self.name

class ServiceSchedule(models.Model):
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name='schedules',
        verbose_name='Veículo'
    )
    
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.PROTECT,
        related_name='schedules',
        verbose_name='Tipo de Serviço'
    )
    
    scheduled_date = models.DateTimeField(
        verbose_name='Data Agendada'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='agendado',
        verbose_name='Status'
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        verbose_name = 'Agendamento de Serviço'
        verbose_name_plural = 'Agendamentos de Serviços'
        
    def __str__(self):
        return f"{self.vehicle} - {self.service_type} - {self.scheduled_date.strftime('%d/%m/%Y %H:%M')}"

class ServiceOrder(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('aguardando_pecas', 'Aguardando Peças'),
        ('aguardando_aprovacao', 'Aguardando Aprovação'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name='service_orders',
        verbose_name='Veículo'
    )
    
    schedule = models.OneToOneField(
        ServiceSchedule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='service_order',
        verbose_name='Agendamento'
    )
    
    start_date = models.DateTimeField(
        verbose_name='Data de Início',
        default=timezone.now
    )
    
    end_date = models.DateTimeField(
        verbose_name='Data de Conclusão',
        null=True,
        blank=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto',
        verbose_name='Status'
    )
    
    diagnosis = models.TextField(
        verbose_name='Diagnóstico',
        blank=True,
        null=True
    )
    
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Custo Total',
        default=0
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        
    def __str__(self):
        return f"OS #{self.id} - {self.vehicle} - {self.status}"

class ServiceItem(models.Model):
    service_order = models.ForeignKey(
        ServiceOrder,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Ordem de Serviço'
    )
    
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.PROTECT,
        related_name='service_items',
        verbose_name='Tipo de Serviço'
    )
    
    description = models.TextField(
        verbose_name='Descrição do Serviço',
        blank=True,
        null=True
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço',
        default=0
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        verbose_name = 'Item de Serviço'
        verbose_name_plural = 'Itens de Serviço'
        
    def __str__(self):
        return f"{self.service_type} - {self.service_order}"

class PartUsage(models.Model):
    service_order = models.ForeignKey(
        ServiceOrder,
        on_delete=models.CASCADE,
        related_name='parts_used',
        verbose_name='Ordem de Serviço'
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='usages',
        verbose_name='Produto/Peça'
    )
    
    quantity = models.IntegerField(
        verbose_name='Quantidade',
        default=1
    )
    
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço Unitário',
        default=0
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        verbose_name = 'Uso de Peça'
        verbose_name_plural = 'Uso de Peças'
        
    def __str__(self):
        return f"{self.product.name_product} ({self.quantity}) - OS #{self.service_order.id}"
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price

class MaintenanceHistory(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='maintenance_history',
        verbose_name='Veículo'
    )
    
    service_order = models.ForeignKey(
        ServiceOrder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='maintenance_records',
        verbose_name='Ordem de Serviço'
    )
    
    maintenance_date = models.DateTimeField(
        verbose_name='Data da Manutenção',
        default=timezone.now
    )
    
    description = models.TextField(
        verbose_name='Descrição da Manutenção'
    )
    
    mileage = models.IntegerField(
        verbose_name='Quilometragem',
        default=0
    )
    
    next_maintenance_date = models.DateField(
        verbose_name='Data da Próxima Manutenção',
        null=True,
        blank=True
    )
    
    next_maintenance_mileage = models.IntegerField(
        verbose_name='Quilometragem para Próxima Manutenção',
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        verbose_name = 'Histórico de Manutenção'
        verbose_name_plural = 'Históricos de Manutenção'
        
    def __str__(self):
        return f"{self.vehicle} - {self.maintenance_date.strftime('%d/%m/%Y')}"
