import os
from InvoiceGenerator.pdf import SimpleInvoice
from tempfile import NamedTemporaryFile
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
# choose english as language
os.environ["INVOICE_LANG"] = "en"

def generateInvoice(customer_name,order_item,pk):
    client = Client(customer_name)
    provider = Provider('Pick a Book', bank_account='2600420569', bank_code='2010')
    creator = Creator('Pick a Book')
    invoice = Invoice(client, provider, creator)
    invoice.currency="Rs. "
    invoice.currency_locale = 'en_IN.UTF-8'
    invoice.date=order_item.date_added.date()
    invoice.add_item(Item(order_item.quantity, order_item.product.price, description=order_item.product.name))
    pdf = SimpleInvoice(invoice)
    pdf.gen("static/invoices/invoices_"+str(pk)+".pdf", generate_qr_code=False)
    