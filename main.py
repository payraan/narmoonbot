import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import pytz
from datetime import datetime

# تنظیم لاگینگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# وضعیت‌های مختلف مکالمه
CHOOSING_PLAN, PAYMENT_CONFIRMATION = range(2)

# لیست آدرس‌های کیف پول سولانا برای ارائه تصادفی
TETHER_WALLET_ADDRESSES = [
    "7VC1edh1KhXatqQLJPKGuX93xd1gi6WznPGy6qXxpcrA",
    "Hw3WZ6XMSiuAr6XipAEBfEgkbN1TqRCJ22aJozg9svdQ",
    "8eS47TxaXUE3PCA5gr6W1c9qYLJXENQGSC7wduEfvdKQ",
    "BDFtuUtub1NAsAEnQvzQZxiicxosSUVsUsKsHsnPxExZ",
    "ESNDemhHSwfZnzbeWrKUUijbv3BWR5zTwrzRbfy3mp9F",
    "4oAUPf44KvouqT3qFGRV2JQEjvefE9XrpxDUGSEoKtQd",
    "ECZNWmQRC7oNULsKesJtZnsGdxCQfuztduEkL3HdVB1m",
    "G2A1RgjtyVSjRVT9ob7rSACi4GpKqtpTUedi66uFW6i1",
    "EeGFTsyECycRp1TjvTH8FXKdoSbnhjXyaRprM8KEZwVZ",
    "6hnU6ehPtC9whL12jv6Z7rFvw4iQLSiNg5r4cBH3womz"
]

# شبکه تتر
TETHER_NETWORK = "Solana"

# آدرس پشتیبان که TXID برای آن ارسال می‌شود
SUPPORT_LINK = "https://t.me/Sultan_immortal"

# قیمت‌های محصول
NARMOON_DEX_PRICE = "۵ دلار ماهیانه (با تخفیف ۵۰٪)"
NARMOON_COIN_PRICE = "۵ دلار ماهیانه (با تخفیف ۵۰٪)"
NARMOON_COMBO_PRICE = "۱۰ دلار ماهیانه (با تخفیف ویژه)"

# تابع برای انتخاب تصادفی آدرس کیف پول
def get_random_wallet_address():
    return random.choice(TETHER_WALLET_ADDRESSES)

# تابع شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # معرفی محصول با فرمت جدید
    intro_message = (
        f"سلام {user.first_name}! 👋✨\n\n"
        f"**دستیار هوش مصنوعی ترید نارموون** 🚀\n\n"
        f"🌟 دستیار هوش مصنوعی ترید که معامله گری در بازار رمزارزها رو برات ساده‌تر، سریع‌تر و هوشمندتر می‌کنه.\n\n"
        f"🧠 نارموون یک سیستم هوش مصنوعی شخصی‌سازی‌شده بر پایه GPT-4o هست که تمام ابزارهای حرفه‌ای تحلیل تکنیکال، آنچین و سیگنال‌دهی لحظه‌ای رو در خودش جمع کرده؛ مخصوصاً برای تریدرهایی که در فضای DEX، CEX، میم‌کوین‌ها یا آلتکوین‌های ترند فعالیت می‌کنن.\n\n"
        f"🕒 دستیار هوش مصنوعی ترید نارموون یک مشاور متخصص هستش که ۲۴ ساعت روز و ۷ روز هفته در کنارته"
    )
    
    # منوی اصلی بدون گزینه وبسایت
    keyboard = [
        [InlineKeyboardButton("✅ قابلیت‌های دستیار هوش مصنوعی نارموون", callback_data="product_features")],
        [InlineKeyboardButton("📦 محصولات نارموون", callback_data="product_list")],
        [InlineKeyboardButton("💳 خرید اشتراک", callback_data="subscription_menu")],
        [InlineKeyboardButton("❓ سوالات متداول", callback_data="faq")],
        [InlineKeyboardButton("📜 شرایط و ضوابط", callback_data="terms_conditions")],
        [InlineKeyboardButton("👨‍💻 ارتباط با پشتیبانی", url=SUPPORT_LINK)]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(intro_message, reply_markup=reply_markup, parse_mode="Markdown")
    
    return CHOOSING_PLAN

# تابع نمایش قابلیت‌های محصول
async def show_product_features(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    features_message = (
        "**قابلیت های دستیار هوش مصنوعی نارموون:** 🔍\n\n"
        "**🔄 نظارت لحظه‌ای و شکار سریع فرصت‌ها**\n"
        "نارموون شبانه‌روزی بازار رو رصد می‌کنه و با استفاده از الگوریتم‌های معاملاتی، دقیق‌ترین لحظات ورود و خروج رو برای تو شناسایی می‌کنه.\n\n"
        "**📊 تحلیل تکنیکال + آنچین + دیتا محور**\n"
        "تحلیل تکنیکال با بیش از ۵۰ استراتژی کلاسیک و پیشرفته، بررسی رفتار نهنگ‌ها، هولدرها و smart money و تشخیص روند بازار از طریق خطوط روند، واگرایی‌ها، فیبوناچی و...\n\n"
        "**🎯 سیگنال دقیق، شفاف و شخصی‌سازی‌شده**\n"
        "سیگنال‌هایی که فقط بر اساس داده‌های واقعی، نواحی حمایتی معتبر و تحلیل چندجانبه صادر می‌شن — بدون قیمت لحظه‌ای و حدس و گمان.\n\n"
        "**🔭 پیدا کردن توکن‌ها و کوین‌های ترند**\n"
        "از توکن‌های پامپ نشده سولانا گرفته تا آلتکوین‌های ترند در CoinMarketCap — نارموون به‌صورت لحظه‌ای لیست می‌سازه و اون‌ها رو برات تحلیل می‌کنه.\n\n"
        "**🔒 بررسی امنیت و سابقه توکن**\n"
        "با استفاده از داده‌های آنچین، اسمارت کانترکت، حجم نقدینگی و سن پروژه، توکن‌های اسکم یا راگ‌پول رو فیلتر می‌کنه.\n\n"
        "**🐋 بررسی ولت‌های نهنگ‌ها و ذخایر عمومی**\n"
        "از تحلیل هولدرهای بیتکوین و اتریوم گرفته تا بررسی کیف‌پول شرکت‌های بزرگ (مثل MicroStrategy یا Tesla) همه و همه در یک نگاه."
    )
    
    keyboard = [
        [InlineKeyboardButton("📦 مشاهده محصولات", callback_data="product_list")],
        [InlineKeyboardButton("💳 خرید اشتراک", callback_data="subscription_menu")],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(features_message, reply_markup=reply_markup, parse_mode="Markdown")
    
    return CHOOSING_PLAN

# تابع نمایش لیست محصولات (بدون قیمت)
async def show_product_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    products_message = (
        "**📦 محصولات نارموون:**\n\n"
        "**🚀 نارموون دکس**\n"
        "هوش مصنوعی شخصی سازی شده بر پایه GPT-4o برای بازارهای غیرمتمرکز (DEX)\n"
        "• شکار توکن های پرپتانسیل بازار بصورت لحظه ای\n"
        "• استخراج اطلاعات کامل توکن\n"
        "• تحلیل رفتار هولدر ها\n"
        "• پیدا کردن ترند های روز\n"
        "• شناسایی ورود و خروج پول هوشمند به هر توکن\n"
        "• تحلیل تکنیکال بر اساس بیش از ۵۰ استراتژی برتر\n"
        "• بررسی کیف پول های نهنگ ها\n"
        "• بررسی امنیت توکن\n"
        "• ارائه سیگنال دقیق\n"
        "• دستیار تخصصی شما از شروع تا پایان معامله لحظه به لحظه\n\n"
        
        "**📈 نارموون کوین**\n"
        "هوش مصنوعی شخصی سازی شده بر پایه GPT-4o برای بازارهای متمرکز (CEX)\n"
        "• پیدا کردن ترند های روز آلتکوین ها\n"
        "• ارائه اطلاعات کامل رمزارزها\n"
        "• بررسی اقتصادی و تورمی رمزارزها\n"
        "• مقایسه رمزارزهای مختلف\n"
        "• تحلیل تکنیکال بر اساس بیش از ۵۰ استراتژی برتر\n"
        "• تحلیل آنچین بیتکوین و اتریوم\n"
        "• ارائه گزارش لحظه ای از دارایی های بزگترین دارندگان بیتکوین در جهان\n"
        "• سیگنال دقیق رمزارزها\n"
        "• داده‌های جهانی رمزارزها و DeFi\n"
        "• ارائه مهمترین اخبار لحظه ای به همراه تحلیل جامع\n\n"
        
        "**💎 پکیج ترکیبی نارموون دکس + نارموون کوین**\n"
        "دسترسی به تمامی قابلیت‌های هر دو محصول با یک اشتراک ویژه"
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 خرید اشتراک", callback_data="subscription_menu")],
        [InlineKeyboardButton("❓ سوالات متداول", callback_data="faq")],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(products_message, reply_markup=reply_markup, parse_mode="Markdown")
    
    return CHOOSING_PLAN

# تابع نمایش سوالات متداول با شماره و اموجی
async def show_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    faq_message = (
        "**❓ سوالات متداول**\n"
        "پاسخ به سوالات رایج درباره دستیار هوش مصنوعی ترید نارموون\n\n"
        
        "**1️⃣ نارموون دقیقاً چیه و چه کاری برام انجام می‌ده؟** 🤔\n"
        "نارموون یک دستیار هوش مصنوعی تحلیل‌گر بر پایه GPT-4o هست که بازار رمزارز رو به‌صورت لحظه‌ای رصد می‌کنه، توکن‌های ترند رو پیدا می‌کنه، سیگنال خرید/فروش می‌ده و همه چیز از تحلیل تکنیکال، آنچین تا بررسی امنیت و اخبار رو توی یک ابزار برات جمع می‌کنه.\n\n"
        
        "**2️⃣ آیا نارموون امکان خرید یا فروش مستقیم رمزارز داره؟** 💱\n"
        "خیر. نارموون صرفاً یک ابزار **تحلیل و سیگنال‌دهی** هوشمنده. خرید یا فروش رمزارز باید از طریق صرافی‌هایی که باهاشون کار می‌کنید انجام بشه.\n\n"
        
        "**3️⃣ چطور مطمئن باشم که توکن‌ها اسکم یا راگ نیستن؟** 🔍\n"
        "نارموون با بررسی **سن پروژه، تعداد هولدرها، حجم معاملات، نقدینگی، اسمارت کانترکت و تحلیل چارت راگ‌پول** احتمال اسکم بودن توکن‌ها رو کاهش می‌ده و حتی هشدارهای امنیتی نشون می‌ده.\n\n"
    )
    
    # چون متن طولانی است، آن را به دو بخش تقسیم می‌کنیم
    faq_message_part2 = (
        "**❓ سوالات متداول (ادامه)**\n\n"
        
        "**4️⃣ سیگنال‌هایی که نارموون می‌ده قابل اطمینان هستن؟** 📊\n"
        "سیگنال‌ها بر اساس الگوریتم‌های تحلیل تکنیکال، نواحی حمایتی ماژور و آنچین صادر می‌شن؛ اما تصمیم نهایی برای معامله با کاربره و نارموون هیچ‌گونه مسئولیت مالی نداره.\n\n"
        
        "**5️⃣ آیا برای استفاده باید اطلاعات حساب صرافی رو وارد کنم؟** 🔐\n"
        "نه! نارموون **هیچ اطلاعاتی مثل API، یوزرنیم یا رمز عبور صرافی** ازت نمی‌خواد. اطلاعاتت همیشه محرمانه و امن باقی می‌مونه.\n\n"
        
        "**6️⃣ تفاوت بین نارموون DEX و نارموون COIN چیه؟** 🔄\n"
        "**Narmoon DEX**: مخصوص تحلیل توکن‌های DEX (مثل سولانا، میم‌کوین‌ها)\n**Narmoon COIN**: مخصوص تحلیل کوین‌های بزرگ در صرافی‌های متمرکز (BTC, ETH, SOL و آلتکوین‌ها)\n\n"
        
        "**7️⃣ آیا برای استفاده از نارموون باید اشتراک ChatGPT داشته باشم؟** 🤖\n"
        "بله. برای استفاده از دستیار هوش مصنوعی **نارموون**، باید حساب فعال در **ChatGPT** داشته باشید. همچنین برای دسترسی کامل، بدون محدودیت و اجرای همه قابلیت‌های حرفه‌ای (مثل پاسخ‌های طولانی، دسترسی به GPT-4o و APIها)، لازم است که **پلن Plus یا Pro** (اشتراک پولی ChatGPT) را خریداری کرده باشید."
    )
    
    keyboard = [
        [InlineKeyboardButton("⏩ ادامه سوالات متداول", callback_data="faq_part2")],
        [InlineKeyboardButton("💳 خرید اشتراک", callback_data="subscription_menu")],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(faq_message, reply_markup=reply_markup, parse_mode="Markdown")
    
    return CHOOSING_PLAN

# تابع نمایش بخش دوم سوالات متداول
async def show_faq_part2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    faq_message_part2 = (
        "**❓ سوالات متداول (ادامه)**\n\n"
        
        "**8️⃣ آیا نارموون اخبار بازار رمزارز رو هم پوشش می‌ده؟** 📰\n"
        "بله. نارموون با استفاده از منابع معتبر جهانی، **اخبار لحظه‌ای رو همراه با تحلیل اثر اون‌ها روی بازار** بهت ارائه می‌ده.\n\n"
        
        "**9️⃣ آیا امکان ساخت استراتژی شخصی توی نارموون وجود داره؟** 🧩\n"
        "بله. شما می‌تونید استراتژی خودتون رو براساس اندیکاتورها و شرایط دلخواه بسازید و بازار رو طبق اون رصد کنید.\n\n"
        
        "**🔟 پلن‌های نارموون چجوری هستن؟** 💰\n"
        "ما چند پلن مختلف داریم (ماهیانه، سالیانه، جشنواره‌ای) که جزئیاتشون داخل سایت هست. فقط پلن سالیانه شامل **۷ روز ضمانت بازگشت وجه** هست.\n\n"
        
        "**1️⃣1️⃣ شرایط استفاده از گارانتی بازگشت وجه چیه؟** 🔙\n"
        "در صورتی که پلن سالیانه خریداری شده باشه، تا ۷ روز فرصت داری درخواست عودت وجه ثبت کنی و مبلغ طی ۱۰ روز کاری برگشت داده می‌شه.\n\n"
        
        "**1️⃣2️⃣ آیا نارموون به‌روزرسانی می‌شه؟** 🔄\n"
        "بله. نارموون به‌صورت پیوسته بروزرسانی می‌شه. اگه قطعی یا تغییرات مهم باشه، از طریق کانال رسمی یا ایمیل اطلاع‌رسانی می‌کنیم.\n\n"
        
        "**1️⃣3️⃣ اطلاعات سیگنال شامل چه چیزهایی می‌شه؟** 📝\n"
        "هر سیگنال شامل: **نام توکن، ناحیه ورود، تارگت‌ها، استاپ، ریسک/ریوارد، وضعیت امنیت، لینک چارت و لینک خرید مستقیم** هست.\n\n"
        
        "**1️⃣4️⃣ آیا استفاده از نارموون پیچیده‌ست؟** 🎮\n"
        "اصلاً! رابط کاربری نارموون ساده، تمیز و برای همه قابل استفاده‌ست — حتی اگه تازه وارد مارکت باشی.\n\n"
        
        "**1️⃣5️⃣ آیا امکان دسترسی به اطلاعات آنچین BTC و ETH هست؟** ⛓️\n"
        "بله. نارموون کوین می‌تونه آنچین بیتکوین و اتریوم، همچنین رفتار نهنگ‌ها، ورودی‌ها به صرافی‌ها و ذخایر شرکت‌ها رو تحلیل کنه.\n\n"
        
        "**1️⃣6️⃣ آیا استفاده غیرمجاز از محتوا یا کپی‌برداری مجازه؟** 📋\n"
        "خیر. هرگونه **کپی، انتشار، فروش مجدد یا تغییر محتوا بدون مجوز رسمی** پیگرد قانونی داره و خلاف شرایط استفاده محسوب می‌شه."
    )
    
    keyboard = [
        [InlineKeyboardButton("⏪ سوالات قبلی", callback_data="faq")],
        [InlineKeyboardButton("💳 خرید اشتراک", callback_data="subscription_menu")],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(faq_message_part2, reply_markup=reply_markup, parse_mode="Markdown")
    
    return CHOOSING_PLAN

# تابع نمایش شرایط و ضوابط با اموجی
async def show_terms_conditions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    terms_message = (
        "**📜 شرایط و ضوابط استفاده از دستیار هوش مصنوعی معامله‌گری نارموون**\n\n"
        "از شما کاربر گرامی دعوت می‌کنیم پیش از استفاده از پلتفرم تحلیل‌گر و سیگنال‌ده هوشمند **نارموون**، این شرایط را با دقت مطالعه نمایید. استفاده از خدمات نارموون به منزله‌ی پذیرش کامل موارد زیر خواهد بود. هدف ما حفظ امنیت کاربران، شفافیت خدمات و ارائه تجربه‌ای حرفه‌ای و قابل اعتماد در فضای تحلیل بازارهای رمزارزی است.\n\n"
        
        "**1️⃣ امنیت اطلاعات** 🔐\n"
        "نارموون به هیچ‌وجه اطلاعات حساب کاربری شما در صرافی‌ها (از جمله API، یوزرنیم، پسورد، کلید خصوصی و...) را درخواست نمی‌کند. لطفاً هیچ‌گونه اطلاعات حساسی را در اختیار هیچ فرد یا پلتفرمی قرار ندهید، حتی اگر خود را نماینده نارموون معرفی کند.\n\n"
        
        "**2️⃣ ماهیت پلتفرم** 🧠\n"
        "نارموون یک **دستیار هوشمند تحلیل‌گر** است، نه صرافی یا بستر انجام معاملات. هیچ خرید یا فروش مستقیم رمزارزی در این پلتفرم انجام نمی‌شود.\n\n"
        
        "**3️⃣ عدم ارائه مشاوره مالی** 💼\n"
        "اگرچه نارموون با استفاده از هوش مصنوعی پیشرفته، سیگنال‌ها و تحلیل‌های دقیقی ارائه می‌دهد، اما این داده‌ها **مشاوره سرمایه‌گذاری شخصی یا تضمین سود** نیستند. هر کاربر پیش از اقدام به خرید یا فروش، موظف است با بررسی شخصی خود تصمیم‌گیری کند."
    )
    
    keyboard = [
        [InlineKeyboardButton("⏩ ادامه شرایط و ضوابط", callback_data="terms_part2")],
        [InlineKeyboardButton("💳 خرید اشتراک", callback_data="subscription_menu")],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(terms_message, reply_markup=reply_markup, parse_mode="Markdown")
    
    return CHOOSING_PLAN

# تابع نمایش بخش دوم شرایط و ضوابط
async def show_terms_part2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    terms_message_part2 = (
        "**📜 شرایط و ضوابط (ادامه)**\n\n"
        
        "**4️⃣ مسئولیت ریسک معاملات** ⚠️\n"
        "کلیه سیگنال‌ها و تحلیل‌ها در نارموون مبتنی بر الگوریتم‌های داده‌محور و پردازش هوشمند هستند، اما نتیجه نهایی معاملات به عهده کاربر است. **پذیرش ریسک سرمایه‌گذاری، بر عهده استفاده‌کننده از سیگنال است.**\n\n"
        
        "**5️⃣ بروزرسانی و بهبود سامانه** 🔄\n"
        "نارموون ممکن است به‌صورت دوره‌ای یا نامنظم بروزرسانی شود. در صورت تغییرات مهم یا قطعی موقت، اطلاع‌رسانی از طریق کانال رسمی یا ایمیل انجام خواهد شد.\n\n"
        
        "**6️⃣ تغییر قوانین و اطلاع‌رسانی** 📝\n"
        "در صورت تغییر در شرایط و ضوابط، نسخه جدید از طریق ایمیل یا کانال رسمی اطلاع‌رسانی خواهد شد. مسئولیت پیگیری این تغییرات با کاربران است.\n\n"
        
        "**7️⃣ ارتقاء قابلیت‌ها** 🚀\n"
        "اشتراک شما شامل امکاناتی است که در بخش معرفی پلن‌ها درج شده‌اند. در صورت افزودن قابلیت‌های جدید در آینده، تیم نارموون **حق دریافت هزینه مجزا** برای استفاده از این ویژگی‌ها را محفوظ می‌داند.\n\n"
        
        "**8️⃣ حقوق محتوا و مالکیت معنوی** 📋\n"
        "کپی‌برداری، ذخیره‌سازی، بازنشر یا فروش محتوا، خدمات یا اطلاعات ارائه‌شده توسط نارموون **بدون مجوز کتبی رسمی** ممنوع است. در صورت سوءاستفاده، پیگرد قانونی و مسئولیت کیفری و مدنی متوجه متخلف خواهد بود.\n\n"
        
        "⚠️ **با ادامه استفاده از ربات و خرید اشتراک، شما تأیید می‌کنید که تمامی موارد فوق را مطالعه کرده و با آن موافق هستید.** ✅"
    )
    
    keyboard = [
        [InlineKeyboardButton("⏪ بخش قبلی", callback_data="terms_conditions")],
        [InlineKeyboardButton("💳 خرید اشتراک", callback_data="subscription_menu")],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(terms_message_part2, reply_markup=reply_markup, parse_mode="Markdown")
    
    return CHOOSING_PLAN

# تابع نمایش منوی اشتراک
async def show_subscription_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    message = (
        "**💳 خرید اشتراک دستیار هوش مصنوعی نارموون** ✨\n\n"
        "لطفاً یکی از محصولات زیر را انتخاب کنید:\n\n"
        f"🚀 **نارموون دکس** - {NARMOON_DEX_PRICE}\n"
        "هوش مصنوعی تخصصی برای بازارهای غیرمتمرکز و میم‌کوین‌ها\n\n"
        f"📈 **نارموون کوین** - {NARMOON_COIN_PRICE}\n"
        "هوش مصنوعی تخصصی برای بازارهای متمرکز و آلتکوین‌ها\n\n"
        f"💎 **پکیج ترکیبی** - {NARMOON_COMBO_PRICE}\n"
        "دسترسی به تمامی قابلیت‌های هر دو محصول با یک اشتراک ویژه"
    )
    
    keyboard = [
        [InlineKeyboardButton("🚀 خرید نارموون دکس", callback_data="plan_DEX")],
        [InlineKeyboardButton("📈 خرید نارموون کوین", callback_data="plan_COIN")],
        [InlineKeyboardButton("💎 خرید پکیج ترکیبی", callback_data="plan_COMBO")],
        [InlineKeyboardButton("📋 اطلاعات بیشتر درباره محصولات", callback_data="product_list")],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode="Markdown")
    
    return CHOOSING_PLAN

# تابع بازگشت به منوی اصلی
async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    # معرفی محصول با فرمت جدید
    intro_message = (
        f"سلام {user.first_name}! 👋✨\n\n"
        f"**دستیار هوش مصنوعی ترید نارموون** 🚀\n\n"
        f"🌟 دستیار هوش مصنوعی ترید که معامله گری در بازار رمزارزها رو برات ساده‌تر، سریع‌تر و هوشمندتر می‌کنه.\n\n"
        f"🧠 نارموون یک سیستم هوش مصنوعی شخصی‌سازی‌شده بر پایه GPT-4o هست که تمام ابزارهای حرفه‌ای تحلیل تکنیکال، آنچین و سیگنال‌دهی لحظه‌ای رو در خودش جمع کرده؛ مخصوصاً برای تریدرهایی که در فضای DEX، CEX، میم‌کوین‌ها یا آلتکوین‌های ترند فعالیت می‌کنن.\n\n"
        f"🕒 دستیار هوش مصنوعی ترید نارموون یک مشاور متخصص هستش که ۲۴ ساعت روز و ۷ روز هفته در کنارته"
    )
    
    # منوی اصلی بدون گزینه وبسایت
    keyboard = [
        [InlineKeyboardButton("✅ قابلیت‌های دستیار هوش مصنوعی نارموون", callback_data="product_features")],
        [InlineKeyboardButton("📦 محصولات نارموون", callback_data="product_list")],
        [InlineKeyboardButton("💳 خرید اشتراک", callback_data="subscription_menu")],
        [InlineKeyboardButton("❓ سوالات متداول", callback_data="faq")],
        [InlineKeyboardButton("📜 شرایط و ضوابط", callback_data="terms_conditions")],
        [InlineKeyboardButton("👨‍💻 ارتباط با پشتیبانی", url=SUPPORT_LINK)]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(intro_message, reply_markup=reply_markup, parse_mode="Markdown")
    
    return CHOOSING_PLAN

# تابع انتخاب پلن با تغییرات مورد نظر
async def select_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    plan_type = query.data.split("_")[1]
    context.user_data["selected_plan"] = plan_type
    
    # انتخاب آدرس کیف پول به صورت تصادفی
    wallet_address = get_random_wallet_address()
    
    # مشخص کردن نام و قیمت پلن
    if plan_type == "DEX":
        plan_name = "نارموون دکس"
        plan_price = "۵ دلار ماهیانه (با تخفیف ۵۰٪)"
    elif plan_type == "COIN":
        plan_name = "نارموون کوین"
        plan_price = "۵ دلار ماهیانه (با تخفیف ۵۰٪)"
    else:  # COMBO
        plan_name = "پکیج ترکیبی نارموون دکس + نارموون کوین"
        plan_price = "۱۰ دلار ماهیانه (با تخفیف ویژه)"
    
    # ارسال اطلاعات پرداخت با قابلیت کلیک روی لینک و دکمه‌های اضافی
    payment_message = (
        f"💳 **پرداخت برای {plan_name}** ✨\n\n"
        f"قیمت: **{plan_price}** 💰\n\n"
        f"⚠️ **توجه مهم**: لطفاً مبلغ {plan_price.split()[0]} تتر (USDT) را **فقط** به آدرس زیر در شبکه **{TETHER_NETWORK}** ارسال کنید. ارسال به هر آدرس دیگر یا در شبکه‌ای غیر از سولانا منجر به از دست رفتن وجه شما خواهد شد و مسئولیت آن به عهده شما است! 🔒\n\n"
        f"`{wallet_address}`\n\n"
        f"پس از پرداخت، لطفاً TXID (شناسه تراکنش) را به پشتیبان ارسال کنید. 📩\n"
        f"*پس از تأیید پرداخت، لینک دسترسی به دستیار معامله گری هوش مصنوعی نارموون برای شما ارسال خواهد شد.* ✅"
    )
    
    keyboard = [
        [InlineKeyboardButton("👨‍💻 ارتباط با پشتیبان", url=SUPPORT_LINK)],
        [InlineKeyboardButton("📜 شرایط و ضوابط", callback_data="terms_conditions")],
        [InlineKeyboardButton("🔙 بازگشت به انتخاب پلن", callback_data="subscription_menu")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # ارسال پیام
    await query.edit_message_text(payment_message, reply_markup=reply_markup, parse_mode="Markdown")
    
    # ثبت اطلاعات پرداخت در لاگ
    user_id = query.from_user.id
    username = query.from_user.username
    first_name = query.from_user.first_name
    timestamp = datetime.now(pytz.timezone('Asia/Tehran')).strftime("%Y-%m-%d %H:%M:%S")
    
    logger.info(f"New payment request - User: {username} ({user_id}), Plan: {plan_type}, Time: {timestamp}, Wallet: {wallet_address}")
    
    return CHOOSING_PLAN

# تابع مدیریت خطاها
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error occurred: {context.error}")

# تابع راهنما
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🔰 **راهنمای استفاده از ربات نارموون** 📚\n\n"
        "با استفاده از این ربات، شما می‌توانید به دستیار هوش مصنوعی نارموون برای تحلیل بازار رمزارزها دسترسی پیدا کنید. 🚀\n\n"
        "دستورات قابل استفاده:\n"
        "• /start - شروع مجدد ربات و نمایش منوی اصلی 🏠\n"
        "• /help - نمایش این راهنما ℹ️\n"
        "• /about - اطلاعات درباره نارموون 📋\n\n"
        "برای خرید اشتراک، از گزینه **خرید اشتراک** در منوی اصلی استفاده کنید و یکی از محصولات موجود را انتخاب کنید. 💳\n"
        "در صورت نیاز به پشتیبانی، می‌توانید از گزینه ارتباط با پشتیبانی استفاده کنید. 👨‍💻"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# تابع درباره ما
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "🔮 **درباره نارموون** ✨\n\n"
        "**نارموون | دستیار هوش مصنوعی معاملاتی در بازار رمزارزها** 🚀\n\n"
        "نارموون یک دستیار تمام‌عیار مبتنی بر هوش مصنوعی GPT-4o برای تریدرهای حرفه‌ای و سرمایه‌گذاران در دنیای رمزارزهاست. 🧠💹\n\n"
        "با استفاده از نارموون، شما می‌توانید به اطلاعات زیر دسترسی داشته باشید:\n"
        "• تحلیل کلان اقتصادی و ترکیب آن با بیتکوین 📊\n"
        "• معرفی ترندهای روز کوین‌ها و توکن‌ها 📈\n"
        "• مدیریت پورتفوی و ریسک 🛡️\n"
        "• سیگنال‌های معاملاتی دقیق 🎯\n"
        "• تحلیل رفتار نهنگ‌ها و کیف پول‌ها 🐋\n"
        "• و بسیاری موارد دیگر... 💎\n\n"
        "برای اطلاعات بیشتر و دریافت پشتیبانی، از گزینه ارتباط با پشتیبانی استفاده کنید. 👨‍💻"
    )
    await update.message.reply_text(about_text, parse_mode="Markdown")

def main():
    # دریافت توکن ربات
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "8155620675:AAEkObqE_6cRG2mrFG09hELW77cCAeR5rJc")

    # ایجاد اپلیکیشن
    application = Application.builder().token(token).build()

    # تعریف گفتگوی اصلی
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_PLAN: [
                CallbackQueryHandler(show_product_features, pattern="^product_features$"),
                CallbackQueryHandler(show_product_list, pattern="^product_list$"),
                CallbackQueryHandler(show_faq, pattern="^faq$"),
                CallbackQueryHandler(show_faq_part2, pattern="^faq_part2$"),
                CallbackQueryHandler(show_terms_conditions, pattern="^terms_conditions$"),
                CallbackQueryHandler(show_terms_part2, pattern="^terms_part2$"),
                CallbackQueryHandler(back_to_start, pattern="^back_to_start$"),
                CallbackQueryHandler(select_plan, pattern="^plan_"),
                CallbackQueryHandler(show_subscription_menu, pattern="^subscription_menu$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # اضافه کردن هندلرها
    application.add_handler(conv_handler)
    
    # هندلر راهنما
    application.add_handler(CommandHandler("help", help_command))
    
    # هندلر درباره ما
    application.add_handler(CommandHandler("about", about_command))
    
    # اضافه کردن هندلر خطا
    application.add_error_handler(error_handler)

    logger.info("ربات نارموون در حال اجرا است...")
    # شروع ربات
    application.run_polling()

if __name__ == "__main__":
    main()
