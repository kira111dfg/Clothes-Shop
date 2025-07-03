from django_elasticsearch_dsl import Document, Index, fields
from .models import Product

product_index = Index('products')

@product_index.document
class ProductDocument(Document):
    brand = fields.ObjectField(properties={
        'title': fields.TextField(),
    })

    class Django:
        model = Product
        fields = [
            'title',
            'description',
        ]

    def prepare_brand(self, instance):
        if instance.brand:
            return {
                'title': instance.brand.title
            }
        return {}

