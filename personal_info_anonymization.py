import re
import pandas as pd
from parstdex import Parstdex
import warnings
warnings.filterwarnings('ignore')

class PersonalInfoAnonymization():
    def __init__(self):    
        #phone_number_pattern
        self.pre_phone_num = "41|44|31|26|45|84|77|21|38|56|51|58|61|24|23|54|71|28|25|87|34|83|74|17|13|66|11|86|76|81|35"
        self.phone_pattern = fr"\b(0({self.pre_phone_num})(\d{{8}}|\d{{5}})|1\d{{2}}|15\d{{2}}|18\d{{2}}|096\d{{2}}|[2-8](\d{{3}}|\d{{4}}))\b"
        #mobile_phone_pattern
        self.mobile_pattern = r'\b09[0-39][0-9]-?[0-9]{3}-?[0-9]{4}\b'
        #national code
        self.national_code = r"\b\d{10}\b"
        # bank card
        self.ws = "[ -]"
        self.bank_card_pattern = fr"\b\d{{16}}|\d{{4}}{self.ws}\d{{4}}{self.ws}\d{{4}}{self.ws}\d{{4}}\b"
        # city pattern
        self.city_names = '|'.join(list(pd.read_csv('Dataset/cities.csv')['City']))
        self.city_name_pattern = fr"\b({self.city_names})\b"
        # company pattern
        self.company_names = '|'.join(list(pd.read_csv('Dataset/company.csv')['company']))
        self.company_name_pattern = fr"\b({self.company_names})\b"
        # first name pattern
        self.first_names = '|'.join(list(pd.read_csv("Dataset/names_dataset.csv")['first_name']))
        self.first_names = re.sub("ي", "ی", self.first_names)
        self.first_name_pattern = fr"\b({self.first_names})\b"
        # last name pattern
        self.last_names = '|'.join(list(pd.read_csv("Dataset/lastname.csv")['lastname']))
        self.last_name_pattern = fr"\b({self.last_names})\b"
        # email pattern
        self.email_pattern = r"\b(\w+([-+(\.|\[dot\])']\w+)*(@|\[at\])\w+([-(\.|\[dot\])]\w+)*(\.|\[dot\])\w+([-(\.|\[dot\])]\w+)*)\b"
        # address pattern
        self.ez_address_identifier = "در |آدرس|که |از |به |نشانی"
        self.non_starter_address_keywords = r"\b(منطقه|طبقه|کوچه|بن بست|پلاک|واحد|خيابان)\b"
        self.relational_address_keywords = r"\b(جنب|رو به رو|روبرو|بالاتر از|پایین‌ تر از|قبل از|بعد از)\b"
        self.special_place = r"\b(مجموعه ورزشی|دانشگاه صنعتی|مغازه|نمایشگاه|سینما|سینمای|پارک|موزه|ورزشگاه|باشگاه|رستوران|کافه|پاساژ|کترینگ|شرکت|دانشگاه|مدرسه|مسجد|راسته|تیمچه|بازار|درمانگاه|بیمارستان|حسینیه|دبستان|دبیرستان|دانشکده|آزمایشگاه|تعمیرگاه|مکانیکی|آتلیه|رادیولوژی|سونوگرافی|نانوایی|بولینگ|تولیدی|کارخانه|قهوه خانه|چای خانه|سفره خانه|فودکورت|مجتمع تجاری|داروخانه|مجلس شورای|ریاست|قوه|دادگاه|دادسرای|بیت |دفتر|حوزه ی علمیه|حرم|فدراسیون)\b"
        self.countries = r"\b(آندورا|امارات متحده عربی|افغانستان|آنتیگوا و باربودا|آنگویلا|آلبانی|ارمنستان|آنگولا|جنوبگان|آرژانتین|ساموآی آمریکا|اتریش|استرالیا|آروبا|جزایر آلند|جمهوری آذربایجان|بوسنی و هرزگوین|باربادوس|بنگلادش|بلژیک|بورکینا فاسو|بلغارستان|بحرین|بوروندی|بنین|سنت بارثلمی|برمودا|برونئی|بولیوی|هلند کارائیب|برزیل|باهاما|بوتان|جزیره بووه|بوتسوانا|بلاروس|بلیز|کانادا|جزایر کوکوس|جمهوری دموکراتیک کنگو|جمهوری آفریقای مرکزی|جمهوری کنگو|سوئیس|ساحل عاج|جزایر کوک|شیلی|کامرون|چین|کلمبیا|کاستاریکا|کوبا|کیپ ورد|کوراسائو|جزیره کریسمس|قبرس|جمهوری چک|آلمان|جیبوتی|دانمارک|دومینیکا|دومینیکا|الجزایر|اکوادور|استونی|مصر|صحرای غربی|اریتره|اسپانیا|اتیوپی|فنلاند|فیجی|جزایر فالکلند|ایالات فدرال میکرونزی|جزایر فارو|فرانسه|گابن|انگلستان|گرانادا|گرجستان|گویان فرانسه|گرنزی|غنا|جبل الطارق|گرینلند|گامبیا|گینه|جزیره گوادلوپ|گینه استوایی|یونان|جزایر جورجیای جنوبی و ساندویچ جنوبی|گواتمالا|گوام|گینه بیسائو|گویان|هنگ کنگ|جزیره هرد و جزایر مک دونالد|هندوراس|کرواسی|هائیتی|مجارستان|اندونزی|جمهوری ایرلند|فلسطین اشغالی (اسرائیل)|جزیره من|هند|قلمروی اقیانوس هند بریتانیا|عراق|ایران|ایسلند|ایتالیا|ادبیات|جامائیکا|اردن|ژاپن|کنیا|قرقیزستان|کامبوج|کیریباتی|کومور|سنت کیتس و نویس|کره شمالی|کره جنوبی|کویت|جزایر کیمن|قزاقستان|لائوس|لبنان|سنت لوسیا|لیختن اشتاین|سری لانکا|لیبریا|لسوتو|لیتوانی|لوکزامبورگ|لتونی|لیبی|مراکش|موناکو|مولداوی|مونته نگرو|سنت مارتین فرانسه|ماداگاسکار|جزایر مارشال|جمهوری مقدونیه|مالی|میانمار|مغولستان|ماکائو|جزایر ماریانای شمالی|مارتینیک|موریتانی|مونتسرات|مالت|موریس|مالدیو|مالاوی|مکزیک|مالزی|موزامبیک|نامیبیا|کالدونیای جدید|نیجر|جزیره نورفولک|نیجریه|نیکاراگوئه|هلند|نروژ|نپال|نائورو|نیوئه|نیوزلند|عمان|پاناما|پرو|پلینزی فرانسه|پاپوآ گینه نو|فیلیپین|پاکستان|لهستان|سنت پیر و ماژلان|جزایر پیت کرن|پورتوریکو|فلسطین|پرتغال|پالائو|پاراگوئه|قطر|ریونیون|رومانی|صربستان|روسیه|رواندا|عربستان سعودی|جزایر سلیمان|سیشل|سودان|سوئد|سنگاپور|سینت هلینا|اسلوونی|سوالبارد و یان ماین|اسلواکی|سیرالئون|سن مارینو|سنگال|سومالی|سورینام|سائوتومه و پرینسیپ|السالوادور|سنت مارتین هلند|سوریه|سوازیلند|جزایر تورکس و کایکوس|چاد|سرزمین های قطب جنوب و جنوبی فرانسه|توگو|تایلند|تاجیکستان|توکلائو|تیمور شرقی|ترکمنستان|تونس|تونگا|ترکیه|ترینیداد و توباگو|تووالو|تایوان|تانزانیا|اوکراین|اوگاندا|جزایر کوچک حاشیه ای آمریکا|ایالات متحده|اروگوئه|ازبکستان|شهر واتیکان|سنت وینسنت و گرنادین|ونزوئلا|جزایر ویرجین بریتانیا|جزایر ویرجین ایالات متحده آمریکا|ویتنام|وانواتو|والیس و فوتونا|ساموآ|یمن|مایوت|آفریقای جنوبی|زامبیا|زیمبابوه)\b"
        self.separators = "،|-|,"
        self.start_address_keywords = r"\b(منطقه|خیابان|بلوار|میدان|بزرگراه|آزادراه|آزاد راه|اتوبان|جاده|محله|کوی|چهار راه|سه‌ راه|کشور|استان|شهرستان|دهستان|روستای|شهرک)\b"
        self.locations = f"{self.countries}"
        self.middle_address_keywords = f"{self.start_address_keywords}|{self.non_starter_address_keywords}|{self.relational_address_keywords}"
        self.starter_keywords = f"{self.ez_address_identifier}|{self.start_address_keywords}|{self.locations}"
        self.address_pattern = fr"(\b({self.starter_keywords})([^\\.]{{{{{{spaces_count}}}}}}({self.middle_address_keywords}|{self.separators})){{{{{{keyword_count}}}}}}( *({self.special_place})? *\w+))|^(({self.middle_address_keywords}|{self.separators}){{{{{{keyword_count}}}}}}( *({self.special_place})? *\w+))"
        # date time pattern
        self.date_time_model = Parstdex()
        # Sheba pattern
        self.sheba_pattern = r"\bIR\d{24}\b"
        #iban pattern
        self.iban_pattern = r"\b(?:(?:IT|SM)\d{2}[A-Z]\d{22}|CY\d{2}[A-Z]\d{23}|NL\d{2}[A-Z]{4}\d{10}|LV\d{2}[A-Z]{4}\d{13}|(?:BG|BH|GB|IE)\d{2}[A-Z]{4}\d{14}|GI\d{2}[A-Z]{4}\d{15}|RO\d{2}[A-Z]{4}\d{16}|KW\d{2}[A-Z]{4}\d{22}|MT\d{2}[A-Z]{4}\d{23}|NO\d{13}|(?:DK|FI|GL|FO)\d{16}|MK\d{17}|(?:AT|EE|KZ|LU|XK)\d{18}|(?:BA|HR|LI|CH|CR)\d{19}|(?:GE|DE|LT|ME|RS)\d{20}|IL\d{21}|(?:AD|CZ|ES|MD|SA)\d{22}|PT\d{23}|(?:BE|IS)\d{24}|(?:FR|MR|MC)\d{25}|(?:AL|DO|LB|PL)\d{26}|(?:AZ|HU)\d{27}|(?:GR|MU)\d{28})\b"
        #url pattern
        self.url_pattern =  r"\b((https|http|ftp):\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)\b"
        # complex verb pattern
        self.verb_postfix = r"(م|ی|یم|ید|ند)"
        self.complex_verb_pattern = fr"به دنیا (خواهد )?آمد{self.verb_postfix}?|شادی (می‌)?(کرد|کن){self.verb_postfix}?|باران (می‌)?(بارد|بارید|زد)|مهیا (می‌)?(کرد|کن){self.verb_postfix}?"
        
    def number_normalizer(self, text):
        persian_numbers = "۰۱۲۳۴۵۶۷۸۹"
        english_numbers = "0123456789"
        arabic_numbers = "٠١٢٣٤٥٦٧٨٩"

        translation_from_persian = str.maketrans(persian_numbers, english_numbers)
        translation_from_arabic = str.maketrans(arabic_numbers, english_numbers)

        return text.translate(translation_from_persian).translate(translation_from_arabic)
    
    def hide_phone(self, text):
        margin = 0
        for matched in re.finditer(self.phone_pattern, text):
            start, end = matched.span()
            text = text[:start-margin] + "<#شماره-تلفن-ثابت>" + text[end-margin:]
            margin += (end-start) - len("<#شماره-تلفن-ثابت>")
        return text
    
    def hide_mobile_num(self, text):
        margin = 0
        for matched in re.finditer(self.mobile_pattern, text):
            start, end = matched.span()
            text = text[:start-margin] + \
                "<#شماره-تلفن-همراه>" + text[end-margin:]
            margin += (end-start) - len("<#شماره-تلفن-همراه>")
        return text

    def hide_national_code(self, text):
        def is_national_code(ncode):
            if len(ncode) != 10:
                return 0
            sum = 0
            nocode = str(ncode)
            for i in range(len(ncode)-1):
                sum += int(ncode[i])*(10-i)
            sum = sum % 11
            flag = 0
            if sum == 1 or sum == 2:
                if int(ncode[9]) == sum:
                    flag = 1
            else:
                if 11-int(ncode[9]) == sum:
                    flag = 1
            return flag
        margin = 0
        for matched in re.finditer(self.national_code, text):
            start, end = matched.span()
            if is_national_code(matched.group(0).strip()):
                text = text[:start-margin] + \
                    "<#کد-ملی-معتبر>" + text[end-margin:]
                margin += (end-start) - len("<#کد-ملی-معتبر>")
            else:
                text = text[:start-margin] + \
                    "<#کد-ملی-نامعتبر>" + text[end-margin:]
                margin += (end-start) - len("<#کد-ملی-نامعتبر>")
        return text

    def hide_bank_card(self, text):
        def card_num_validation(card_num):
            sum = 0
            for idx, digit in enumerate(card_num):
                digit = int(digit)
                if not idx % 2:
                    sum += digit*2 if digit*2 < 9 else digit*2-9
                else:
                    sum += digit
            if not sum % 10:
                return True
        margin = 0
        for matched in re.finditer(self.bank_card_pattern, text):
            start, end = matched.span()
            if card_num_validation(re.sub(self.ws, "", matched.group(0))):
                text = text[:start-margin] + \
                    "<#شماره-کارت-معتبر>" + text[end-margin:]
                margin += (end-start) - len("<#شماره-کارت-معتبر>")
            else:
                text = text[:start-margin] + \
                    "<#شماره-کارت-نامعتبر>" + text[end-margin:]
                margin += (end-start) - len("<#شماره-کارت-نامعتبر>")
        return text

    def hide_city(self, text):
        margin = 0
        for matched in re.finditer(self.city_name_pattern, text):
            start, end = matched.span()
            text = text[:start-margin] + "<#نام-شهر>" + text[end-margin:]
            margin += (end-start) - len("<#نام-شهر>")
        return text

    def hide_company(self, text):
        margin = 0
        for matched in re.finditer(self.company_name_pattern, text):
            start, end = matched.span()
            text = text[:start-margin] + "<#نام-شرکت>" + text[end-margin:]
            margin += (end-start) - len("<#نام-شرکت>")
        return text

    def hide_name(self, text):
        margin = 0
        complex_verb_spans = []
        for m in re.finditer(self.complex_verb_pattern, text):
            complex_verb_spans.append(m.span())
        for matched in re.finditer(self.first_name_pattern, text):
            start, end = matched.span()
            flag_name = False
            for interval in complex_verb_spans:
              if end < interval[0]:
                break
              if start >= interval[0] and end <= interval[1]:
                flag_name = True
            if not flag_name :
                text = text[:start-margin] + "<#نام-شخص>" + text[end-margin:]
                margin += (end-start) - len("<#نام-شخص>")
        return text
    
    def hide_lname(self, text):
        margin = 0
        for matched in re.finditer(self.last_name_pattern, text):
            start, end = matched.span()
            text = text[:start-margin] + "<#نام-خانوادگی>" + text[end-margin:]
            margin += (end-start) - len("<#نام-خانوادگی>")
        return text

    def hide_email(self, text):
        margin = 0
        for matched in re.finditer(self.email_pattern, text):
            start, end = matched.span()
            text = text[:start-margin] + "<#آدرس-ایمیل>" + text[end-margin:]
            margin += (end-start) - len("<#آدرس-ایمیل>")
        return text

    def hide_address(self, text):
        proposition = "در|از|که|به"
        for keyword_count in range(10, 0, -1):
            count_pattern = self.address_pattern.format(
                keyword_count=keyword_count, spaces_count="0,20")
            margin = 0
            for matched in re.finditer(count_pattern, text):
                start, end = matched.span()
                prop = re.search(fr"({proposition}) .+", matched.group(0))
                if prop:
                    prop_len = len(prop.group(1))
                    start+=prop_len
                text = text[:start-margin] + " <#آدرس> " + text[end-margin:]
                margin += (end-start) - len(" <#آدرس> ")
        return text       

    def merge_addresses(self, text):
        res = text.split()
        for idx, word in enumerate(res):
            if word == "<#آدرس>":
                if res[idx+1] == "<#نام-شهر>":
                    res.pop(idx+1)
                elif res[idx+1] == "شهر" and res[idx+2] == "<#نام-شهر>":
                    res.pop(idx+1)
                    res.pop(idx+1)
        return " ".join(res)

    def hide_date_time(self,text):
        margin = 0  
        for x in self.date_time_model.extract_span(text)['date']:
            start , end = x
            text = text[:start-margin] + \
                        " <#تاریخ> " + text[end-margin:]
            margin += (end-start) - len(" <#تاریخ> ")
        margin = 0
        for x in self.date_time_model.extract_span(text)['time']:
            start , end = x
            text = text[:start-margin] + \
                        " <#زمان> " + text[end-margin:]
            margin += (end-start) - len(" <#زمان> ")
        return text

    def hide_sheba(self,text):
      margin = 0
      for matched in re.finditer(self.sheba_pattern, text):
            start, end = matched.span()
            text = text[:start-margin] + "<#شماره-شبا>" + text[end-margin:]
            margin += (end-start) - len("<#شماره-شبا>")
      return text
    
    def hide_iban(self,text):
      margin = 0
      for matched in re.finditer(self.iban_pattern, text):
            start, end = matched.span()
            text = text[:start-margin] + "<#شماره-ایبان>" + text[end-margin:]
            margin += (end-start) - len("<#شماره-ایبان>")
      return text

    def hide_url(self, text):
        margin = 0
        for matched in re.finditer(self.url_pattern, text):
            start, end = matched.span()
            text = text[:start-margin] + "<#تارنما>" + text[end-margin:]
            margin += (end-start) - len("<#تارنما>")
        return text

    def run(self, text):
        text = self.number_normalizer(text)
        text = self.hide_address(text)
        text = self.hide_iban(text)
        text = self.hide_phone(text)
        text = self.hide_mobile_num(text)
        text = self.hide_national_code(text)
        text = self.hide_bank_card(text)
        text = self.hide_sheba(text)
        text = self.hide_email(text)
        text = self.hide_url(text)
        text = self.hide_company(text)
        text = self.hide_date_time(text)
        text = self.hide_city(text)
        text = self.merge_addresses(text)
        text = self.hide_name(text)
        text = self.hide_lname(text)
        return text

