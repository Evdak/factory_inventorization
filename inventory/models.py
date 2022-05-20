import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib import messages


# Create your models here.
SHIFTS = (
    ('1', 'Первая смена'),
    ('2', 'Вторая смена'),
)

UNITS = (
    ('шт', 'шт'),
    ('кг', 'кг'),
)

TYPES = (
    ('Камаз', 'Камаз'),
    ('Ярославль', 'Ярославль'),
)


class HeatExchanger(models.Model):
    heatExchanger_name = models.CharField('Наименование', max_length=200)
    heatExchanger_number = models.CharField('Чертежный номер', max_length=200)
    heatExchanger_count = models.FloatField(
        'Количество на складе', blank=True, default=0, validators=[
            MinValueValidator(0)
        ]
    )

    class Meta:
        verbose_name = 'Теплобменник'
        verbose_name_plural = 'Теплобменники'

    def __str__(self) -> str:
        return f"{self.heatExchanger_name}, {self.heatExchanger_number}"


class Product(models.Model):
    product_name = models.CharField('Наименование', max_length=200)
    product_number = models.CharField('Чертежный номер', max_length=200)
    product_count = models.FloatField(
        'Количество на складе', blank=True, default=0, validators=[
            MinValueValidator(0)
        ]
    )
    product_unit = models.CharField(
        'Единица измерения', max_length=20, choices=UNITS)
    product_consumption = models.FloatField('Расход на 1 ЖМТ')
    product_reserves = models.IntegerField(
        'На сколько ЖМТ хватит', blank=True, null=True, default=0, editable=False)
    # product_type = models.CharField(
    #     'Вид теплообменника', max_length=20, choices=TYPES)
    product_type = models.ManyToManyField(
        HeatExchanger, verbose_name='Теплообменники')
    # product_price = models.IntegerField('Цена без НДС', blank=True, null=True)

    # product_export_only = models.BooleanField(
    #     "Доступен для ухода", default=False)

    def save(self, *args, **kwargs):
        self.product_reserves = self.get_product_reserves()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'

    def __str__(self) -> str:
        return f"{self.product_name}, {self.product_number}"

    def get_product_reserves(self):
        verbose_name = "На сколько ЖМТ хватит"
        try:
            return (round(self.product_count / self.product_consumption, 2))
        except ZeroDivisionError:
            return 0


# @receiver(post_save, sender=Product)
# def notify_users(sender, created, instance, **kwargs):
#     # for el in
#     # Product.objects.all().update(product_reserves="get_product_reserves")
#     # print(el.get_product_reserves())
#     # el.product_reserves = el.get_product_reserves()


class Company(models.Model):
    company_name = models.CharField('Название', max_length=200)
    company_inn = models.CharField('ИНН', max_length=200)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self) -> str:
        return self.company_name


class Import(models.Model):
    import_date = models.DateField('Дата прихода')
    import_shift = models.CharField('Смена', choices=SHIFTS, max_length=30)
    import_name = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, null=True, blank=True,  verbose_name='Наименование изделия')
    import_name_heat = models.ForeignKey(
        HeatExchanger, on_delete=models.DO_NOTHING, null=True, blank=True,  verbose_name='Наименование теплообменника')
    import_count = models.FloatField('Количество', validators=[
        MinValueValidator(0)
    ]
    )
    import_unit = models.CharField(
        'Единица измерения', max_length=20, choices=UNITS)
    import_from = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, verbose_name='От кого')
    import_document = models.CharField('Документ прихода', max_length=300)
    # import_price = models.IntegerField('Цена покупки')

    class Meta:
        verbose_name = 'Приход'
        verbose_name_plural = 'Приходы'

    def __str__(self) -> str:
        return f"{self.import_name}, {self.import_count}"


@receiver(post_save, sender=Import)
def notify_users(sender, created, instance, **kwargs):
    # print(instance.__str__())
    if created:
        if instance.import_name_heat:
            HeatExchanger.objects.filter(id=instance.import_name_heat.id).update(heatExchanger_count=(
                instance.import_name_heat.heatExchanger_count + instance.import_count))
            _product_type = instance.import_name_heat
            for el in Product.objects.filter(product_type=_product_type):
                el.product_count = el.product_count - \
                    (instance.import_count * el.product_consumption)
                el.save()

        else:
            Product.objects.filter(id=instance.import_name.id).update(product_count=(
                instance.import_name.product_count + instance.import_count))
            for el in Product.objects.all():
                el.save()
        # Product.objects.filter(id=instance.import_name.id).update(
        #     product_reserves=(instance.import_name.get_product_reserves()))


class Export(models.Model):
    export_date = models.DateField('Дата ухода')
    export_shift = models.CharField('Смена', choices=SHIFTS, max_length=30)
    export_name = models.ForeignKey(
        HeatExchanger,
        on_delete=models.DO_NOTHING,
        verbose_name='Наименование изделия',
        # limit_choices_to={'product_export_only': True}
    )
    export_count = models.FloatField('Количество', validators=[
        MinValueValidator(0)
    ]
    )
    export_unit = models.CharField(
        'Единица измерения', max_length=20, choices=UNITS)
    export_from = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, verbose_name='Кому')
    export_document = models.CharField('Документ ухода', max_length=300)
    export_duration = models.IntegerField('Отсрочка платежа (дней)')
    export_receive_date = models.DateField(
        'Дата посутпления платежа', blank=True, null=True, editable=False)
    # export_price = models.IntegerField('Цена продажи')

    class Meta:
        verbose_name = 'Отгрузка'
        verbose_name_plural = 'Отгрузки'

    def save(self, *args, **kwargs):
        self.export_receive_date = self.export_date + \
            datetime.timedelta(days=self.export_duration)
        if self.export_count >= self.export_name.heatExchanger_count:
            # super().save(*args, **kwargs)
            raise ValidationError("Количество больше, чем есть на складе")
        else:
            super().save(*args, **kwargs)

    def get_receive_date(self):
        verbose_name = "Поступление платежа"

        return self.export_date + datetime.timedelta(days=self.export_duration)


@receiver(post_save, sender=Export)
def notify_users(sender, created, instance, **kwargs):
    if created:
        HeatExchanger.objects.filter(id=instance.export_name.id).update(heatExchanger_count=(
            instance.export_name.heatExchanger_count - instance.export_count))


class Defect(models.Model):
    defect_date = models.DateField('Дата отправки в брак')
    defect_shift = models.CharField('Смена', choices=SHIFTS, max_length=30)
    defect_name = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='Наименование изделия')
    defect_name_heat = models.ForeignKey(
        HeatExchanger, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='Наименование теплообменника')
    defect_count = models.FloatField(
        'Количество', validators=[
            MinValueValidator(0)
        ]
    )
    defect_unit = models.CharField(
        'Единица измерения', max_length=20, choices=UNITS)

    class Meta:
        verbose_name = 'Брак'
        verbose_name_plural = 'Брак'

    def __str__(self) -> str:
        return f"{self.defect_name if self.defect_name else self.defect_name_heat}, {self.defect_count} {self.defect_unit}, {self.defect_date}"


@receiver(post_save, sender=Defect)
def notify_users(sender, created, instance, **kwargs):
    if created:
        if instance.defect_name_heat:
            _product_id = instance.defect_name_heat.id
            for el in HeatExchanger.objects.filter(id=_product_id):
                if el.heatExchanger_count - instance.defect_count >= 0:
                    el.heatExchanger_count = el.heatExchanger_count - instance.defect_count
                    el.save()
                else:
                    raise ValidationError('Количество больше, чем на складе')
        else:
            _product_id = instance.defect_name.id
            for el in Product.objects.filter(id=_product_id):
                if el.product_count - instance.defect_count >= 0:
                    el.product_count = el.product_count - instance.defect_count
                    el.save()
                else:
                    raise ValidationError('Количество больше, чем на складе')
                # Product.objects.filter(id=instance.defect_name.id).update(
                #     product_reserves=(instance.defect_name.get_product_reserves()))


class Trash(models.Model):
    trash_date = models.DateField('Дата отправки в брак')
    trash_shift = models.CharField('Смена', choices=SHIFTS, max_length=30)
    trash_name = models.ForeignKey(
        Defect,
        on_delete=models.SET_NULL,
        verbose_name='Наименование изделия',
        null=True
    )
    trash_name_str = models.CharField(
        'Наименование изделия', max_length=200, blank=True, null=True, editable=False)
    trash_count = models.FloatField(
        'Количество', validators=[
            MinValueValidator(0)
        ]
    )
    trash_unit = models.CharField(
        'Единица измерения', max_length=20, choices=UNITS)

    class Meta:
        verbose_name = 'Списание'
        verbose_name_plural = 'Списания'

    def __str__(self) -> str:
        return f"{self.trash_name}, {self.trash_count} {self.trash_unit}, {self.trash_date}"

    def save(self, *args, **kwargs):
        self.trash_name_str = self.trash_name.__str__()
        if self.trash_name.defect_count - self.trash_count < 0:
            raise ValidationError("Количество больше, чем в браке")
        else:
            super().save(*args, **kwargs)


@receiver(post_save, sender=Trash)
def notify_users(sender, created, instance, **kwargs):
    if created:
        _trash_id = instance.trash_name.id
        for el in Defect.objects.filter(id=_trash_id):
            el.defect_count = el.defect_count - instance.trash_count
            if el.defect_count == 0:
                # instance.trash_name = el.
                # print(dir(el))
                print(instance.trash_name_str)
                el.delete()
            else:
                el.save()
