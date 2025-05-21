from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Токен 
TOKEN = "7966881645:AAHvTn14-ZELil_rV2zDU2lFQlNenqZCCk8"

# Клавиатура с основными командами
main_keyboard = ReplyKeyboardMarkup(
    [['/start', '/help'],
     ['/about', '/how_it_works'],
     ['/advantages', '/order']],
    resize_keyboard=True
)

def start(update: Update, context: CallbackContext) -> None:
    """Приветственное сообщение"""
    message = (
        "🚗 *Добро пожаловать в бот для аппарата мойки автомобильных ковриков!*\n\n"
        "Здесь вы можете узнать о нашем инновационном устройстве для быстрой и эффективной мойки ковриков.\n\n"
        "Используйте меню или команды для навигации:"
    )
    update.message.reply_text(message, reply_markup=main_keyboard, parse_mode='Markdown')

def help_command(update: Update, context: CallbackContext) -> None:
    """Помощь по командам"""
    help_text = (
        "*Доступные команды:*\n"
        "/start - начать работу с ботом\n"
        "/help - помощь по командам\n"
        "/about - о нашем проекте\n"
        "/how_it_works - как работает аппарат\n"
        "/advantages - преимущества нашего решения\n"
        "/order - оставить заявку на покупку\n\n"
        "Также вы можете просто написать свой вопрос."
    )
    update.message.reply_text(help_text, parse_mode='Markdown')

def about(update: Update, context: CallbackContext) -> None:
    """Информация о проекте"""
    about_text = (
        "*О нашем проекте*\n\n"
        "Наш аппарат для мойки автомобильных ковриков - это инновационное решение, разработанное в рамках проектной деятельности.\n\n"
        "Основные характеристики:\n"
        "- Автоматизированный процесс мойки\n"
        "- Экономия времени и воды\n"
        "- Компактные размеры\n"
        "- Простота использования\n\n"
        "Устройство предназначено для автомоек, сервисных центров и частного использования."
    )
    update.message.reply_text(about_text, parse_mode='Markdown')

def how_it_works(update: Update, context: CallbackContext) -> None:
    """Принцип работы аппарата"""
    works_text = (
        "*Как работает наш аппарат*\n\n"
        "1. Поместите коврик в специальный отсек\n"
        "2. Выберите программу мойки (интенсивность, использование моющих средств)\n"
        "3. Аппарат автоматически:\n"
        "   - Наносит моющий раствор\n"
        "   - Очищает поверхность щетками\n"
        "   - Тщательно промывает водой\n"
        "   - Отжимает излишки влаги\n"
        "4. Через 5-7 минут коврик чист и почти сух!\n\n"
        "Весь процесс происходит без вашего участия!"
    )
    update.message.reply_text(works_text, parse_mode='Markdown')

def advantages(update: Update, context: CallbackContext) -> None:
    """Преимущества"""
    adv_text = (
        "*Преимущества нашего аппарата*\n\n"
        "✅ В 3 раза быстрее ручной мойки\n"
        "✅ Экономит до 40% воды\n"
        "✅ Бережная очистка без повреждений\n"
        "✅ Удобство и простота использования\n"
        "✅ Компактность - не занимает много места\n"
        "✅ Автоматизация процесса - минимум ручного труда\n\n"
        "Идеальное решение для бизнеса и личного использования!"
    )
    update.message.reply_text(adv_text, parse_mode='Markdown')

def order(update: Update, context: CallbackContext) -> None:
    """Заказ аппарата"""
    order_text = (
        "*Оформление заявки*\n\n"
        "Для заказа нашего аппарата для мойки автомобильных ковриков, пожалуйста, отправьте нам следующую информацию:\n"
        "1. Ваше имя\n"
        "2. Контактный телефон\n"
        "3. Город доставки\n"
        "4. Желаемое количество аппаратов\n\n"
        "Мы свяжемся с вами в ближайшее время для уточнения деталей!"
    )
    update.message.reply_text(order_text, parse_mode='Markdown')
    
    # Сохраняем, что пользователь начал процесс заказа
    context.user_data['expecting_order_info'] = True

def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработка обычных сообщений"""
    if context.user_data.get('expecting_order_info'):
        # Если пользователь отправил данные для заказа
        order_info = update.message.text
        # Здесь можно сохранить информацию в базу данных или отправить на почту
        update.message.reply_text(
            "Спасибо за вашу заявку! Наш менеджер свяжется с вами в течение 24 часов.",
            reply_markup=main_keyboard
        )
        context.user_data['expecting_order_info'] = False
        
        # Можно добавить отправку уведомления администратору
        context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,  # Замените на ID админа
            text=f"Новая заявка!\n\n{order_info}"
        )
    else:
        # Ответ на произвольные вопросы
        update.message.reply_text(
            "Спасибо за ваше сообщение! Для получения информации о нашем аппарате используйте меню команд.",
            reply_markup=main_keyboard
        )

def main() -> None:
    """Запуск бота"""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("about", about))
    dispatcher.add_handler(CommandHandler("how_it_works", how_it_works))
    dispatcher.add_handler(CommandHandler("advantages", advantages))
    dispatcher.add_handler(CommandHandler("order", order))
    
    # Обработчик обычных сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
