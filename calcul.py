import config
import telebot
from telebot import types
from telebot import util


bot = telebot.Telebot(config.token)

user_num1 =''
user_num2 =''
user_proc =''
user_result = None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(massage):
    markup = types.ReplyKeyboardRemove(selective=False)
    
    msg = bot.send_massage(massage.chat.id, 'Hello' + massage.from_user.first_name + 'am bot calculator\nEnter number', reply_markup=markup)
    bot.register_next_step_handler(msg, process_num1_step)

def process_num1_step(massage, user_result = None):
    try:
        global user_num1
              
        if user_result == None:
            user_num1 = int(massage.text)
            
        else:
            user_num1 = str(user_result)    
                        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('+')
        itembtn2 = types.KeyboardButton('-')
        itembtn3 = types.KeyboardButton('*')
        itembtn4 = types.KeyboardButton('/')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    
        msg = bot.send_massage(massage.chat.id, 'Choose the operation', reply_markup=markup)
        bot.register_next_step_handler(msg, process_proc_step) 
    
    except Exception as e:
        bot.reply_to(massage, 'This is not a number....')
    
def process_proc_step(massage):
    try:
        global user_proc     
        
        user_proc = massage.text  
        
        markup =  types.ReplyKeyboardRemove(selective=False)
        
        msg = bot.send_massage(massage.chat.id, 'Enter one more number', reply_markup=markup)
        bot.register_next_step_handler(msg, process_num2_step)
    except Exception as e:
        bot.reply_to(massage, 'You entered something else and everything is going on wrong...')
        
def process_num2_step(massage):
    try:
        global user_num2
           
        user_num2 = int(massage.text)
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)    
        itembtn1 = types.KeyboardButton('Result')
        itembtn2 = types.KeyboardButton('Continue calculation')  
        markup.add(itembtn1, itembtn2)
        
        msg = bot.send_masssage(massage.chat.id, 'Show the result or continue the operation?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_alternative_step)
        
    except Exception as e:
        bot.reply_to(massage, 'It is not a number...')
        
def process_alternative_step(massage):
    try:
        calc()
        
        markup = types.ReplyKeyboardRemove(selective=False)
        
        if massage.text.lower() == 'result':
            bot.send_massage(massage.chat.id, calcResultPrint(), reply_makup=markup)

        elif massage.text.lower() == 'continue the calculation':
            process_num1_step(massage, user_result)
            
    except Exception as e:
        bot.reply_to(massage, 'Something is going on wrong...')
        
        
def calcResultPrint():
    global user_num1, user_num2, user_result
    return "Result:" + str(user_num1) + ' ' + user_proc + ' ' + str(user_num2) + ' = ' + str(user_result)

def calc():
    global user_num1, user_num2, user_proc, user_result
    user_result = eval(str(user_num1) + user_proc + str(user_num2))
    
    return user_result
            
            
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '_main_':
    bot.polling(none_stop=True)
            




