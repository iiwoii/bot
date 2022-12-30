import telebot
from telebot import types
from telebot.types import LabeledPrice, ShippingOption
import const
from geopy.distance import geodesic
import datetime
from ORM import *


book = Book.get(Book.name == 'Hieroglyph AI book (English edition)')
book_str = book.name + ' ' +  book.description + ' ' + book.instructions

provider_token = const.PAYMENTS_TOKEN
bot = telebot.TeleBot(const.API_TOKEN)


PRICES = [LabeledPrice(label='Hieroglyph AI book in English', amount = 135000)]
shipping_options = [
    ShippingOption(id='instant', title='WorldWide Delivery').add_price(LabeledPrice('WordWide Courier',5000)),
    ShippingOption(id='pickup', title='Russia Delivery').add_price(LabeledPrice('Yandex or Pochta Rossii Courier', 1000))]

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn_buy = types.KeyboardButton('Buy your book')
btn_address = types.KeyboardButton('Self-delivery service', request_location=True)
btn_payment = types.KeyboardButton('Payment options')
btn_delivery= types.KeyboardButton('Delivery')
btn_contacts= types.KeyboardButton('Book Review')
btn_about= types.KeyboardButton('About')
btn_help= types.KeyboardButton('Help')
markup_menu.add(btn_buy,btn_address, btn_payment, btn_delivery, btn_contacts, btn_about, btn_help)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "My name is IIWOII bot:) Let`s start our conversation! Make your choice in menu.\n"
                          "You can use /buy to order books, /terms to read Term and Conditions, /start to start conversation from the beginning, /stop to say goodbye to chat", reply_markup=markup_menu)

@bot.message_handler(commands=['stop'])
def send_bye(message):
    bot.reply_to(message, "See you next time",reply_markup=markup_menu)
@bot.message_handler(commands=['term'])

def command_term(message):
    bot.send_message(message.chat.id, 'We use the standard terms of online shopping based on laws of Russian Federation, including the work with personal data')

@bot.message_handler(commands=['buy'])
def command_pay(message):
    bot.send_message(message.chat.id, "No money will be credited from your account.""Use this test card number to pay for your books:'4242 4242 4242 4242 and any exp date and secret code number'""\n This is you demo invoice:")
    bot.send_invoice(message.chat.id,'Hieroglyph AI book','Sci-Fi',provider_token = const.PAYMENTS_TOKEN, currency ='rub',prices=PRICES,photo_url='\hieroglyphaipocketbook.jpg',photo_height=512,photo_width=512,photo_size=512,is_flexible=False, start_parameter='book-example', invoice_payload='some_invoice')

@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id,ok=True,shipping_options=shipping_options, error_message='Oh, something goes wrong, try again later!')

@bot.pre_checkout_query_handler(func=lambda query:True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="Try to pay again in a few minutes")

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,'Thanks for payment, we will proceed your order  as fast as possible!'.format(message.successful_payment.total_amount/100,message.successful_payment.currency))

@bot.message_handler(func=lambda message:True)
def echo_all(message):
    if message.text == 'Delivery':
        bot.reply_to(message, "Express(~ 2h)delivery on weekend with Yandex Taxi, Pochta Rossii courier, Yandex courier", reply_markup=markup_menu)
    elif message.text == 'Book Review':
        bot.reply_to(message, book_str, reply_markup=markup_menu)
    elif message.text == 'Payment options':
        bot.reply_to(message, "Cash, Cards, QR, Wirepayment", reply_markup=markup_menu)
    elif message.text == 'About':
        bot.reply_to(message, "We are the sci-fi books shop, our company works since 2012, our genres are novels, romans, adventures, phylosophy, have a good read!", reply_markup=markup_menu)
    elif message.text == 'Help':
        bot.reply_to(message, "Contact our manager on telegram chat @IIWOII_Group \n or +7 495 764 89 71, vopros@iiwoii.ru ", reply_markup=markup_menu)
    elif message.text == 'Buy your book':
        bot.send_message(message.chat.id,
                         "No money will be credited from your account.""Use this test card number to pay for your books:'4242 4242 4242 4242 and any exp date and secret code number'""\n This is you demo invoice:")
        bot.send_invoice(message.chat.id, 'Hieroglyph AI book', 'Sci-Fi', provider_token=const.PAYMENTS_TOKEN,
                         currency='rub', prices=PRICES, photo_url='\hieroglyphaipocketbook.jpg', photo_height=512,
                         photo_width=512, photo_size=512, is_flexible=False, start_parameter='book-example',
                         invoice_payload='some_invoice')


    else:
        bot.reply_to(message, "OK! You have two options. Use the menu or you may contact our manager @IIWOII_Group", reply_markup=markup_menu)
@bot.message_handler(func=lambda message:True,content_types=['location'])
def magazin_location(message):
    lon = message.location.longitude
    lat = message.location.latitude
    distance = []
    for m in const.MAGAZINS:
        result = geodesic((m['latm'],m['lonm']),(lat,lon)).km
        distance.append(result)
    index = distance.index(min(distance))

    bot.send_message(message.chat.id,'Go here for self-delivery!')
    bot.send_venue(message.chat.id,const.MAGAZINS[index]['latm'],const.MAGAZINS[index]['lonm'],const.MAGAZINS[index]['title'],const.MAGAZINS[index]['address'])


bot.infinity_polling(skip_pending = True)
