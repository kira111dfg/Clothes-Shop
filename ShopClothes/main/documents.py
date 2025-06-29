from django_elasticsearch_dsl import Document, Index, fields
from .models import Product

book_index = Index('products')

@book_index.doc_type
class ProductDocument(Document):
    class Django:
        model = Product
        fields = [
            'title',
            
            'description',
            
        ]