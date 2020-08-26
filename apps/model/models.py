import unicodedata

from django.db import models
from django.contrib import auth
from django.contrib.auth import password_validation
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import check_password, is_password_usable, make_password
from django.contrib.auth.models import PermissionsMixin
from django.utils.crypto import salted_hmac

from django_mysql.models import Model, JSONField

username_validator = UnicodeUsernameValidator


class AbstractModel(Model):
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class AbstractUser(PermissionsMixin):
    username = models.CharField(verbose_name='username', max_length=150, null=True)
    mobile = models.CharField(verbose_name='手机号', max_length=11, db_index=True, unique=True, null=True)
    email = models.EmailField(verbose_name='email', db_index=True, unique=True, null=True)
    password = models.CharField(verbose_name='password', max_length=128)
    is_active = models.BooleanField(verbose_name='active', default=True)

    _password = None
    _is_active = True
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return 'email'

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()

    def save(self, *args, **kwargs):
        if self.mobile or self.email:
            super().save(*args, **kwargs)
            if self._password is not None:
                password_validation.password_changed(self._password, self)
                self._password = None
        else:
            raise Exception('mobile and email is none')

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))
        self.email = self.__class__.objects.normalize_email(self.email)

    def natural_key(self):
        return (self.get_username(),)

    def __str__(self):
        return self.get_username()


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'users'


class Expert(AbstractModel):
    name = models.CharField('专家姓名', max_length=20, db_index=True)
    organization = models.CharField('所属机构', max_length=200, db_index=True)
    department = models.CharField('学院/学部/研究所/部门', max_length=50, null=True)
    keywords = JSONField(verbose_name='专家关键词', null=True)
    personal_introduction = models.TextField('个人简介', null=True)
    birth = models.CharField('出生日期', max_length=20, null=True)
    info_link = models.CharField('专家信息链接', max_length=400, null=True)
    post = models.CharField('职务', max_length=20, null=True)
    title = models.CharField('职称', max_length=50, null=True)
    degree = models.CharField('学历/学位', max_length=50, null=True)
    honorary_titles = models.CharField('荣誉称号', max_length=100, null=True)
    graduated_from = models.CharField('毕业院校', max_length=50, null=True)
    major = models.CharField('专业/学科', max_length=50, null=True)
    research_areas = models.CharField('研究方向', max_length=100, null=True)
    projects = models.TextField('成果', null=True)
    contact = models.CharField('联系方式', max_length=100, null=True)
    province = models.CharField('省份', max_length=30, null=True)
    city = models.CharField('城市', max_length=30, null=True)
    address = models.CharField('办公地点', max_length=100, null=True)
    origins = models.CharField('数据来源', max_length=50, null=True)

    class Meta:
        db_table = 'experts'
        unique_together = ('name', 'organization')


class ActionRecord(AbstractModel):
    page = models.CharField('操作页面', max_length=400)
    action = models.CharField('操作', max_length=100)
    ip = models.CharField('用户ip', max_length=100)
    terminal = models.CharField('操作使用的终端', max_length=100)
    name = models.CharField('用户名', max_length=100, null=True)
    role = models.CharField('用户类型', max_length=100)
    description = models.TextField('用户操作说明')

    class Meta:
        db_table = 'action_records'


class Conference(AbstractModel):
    original_id = models.CharField('源数据id', max_length=100, null=True, unique=True, db_index=True)
    title = models.CharField('论文标题', max_length=100, db_index=True)
    abstract = models.TextField('论文摘要', null=True)
    keywords = JSONField(verbose_name='关键词', null=True)
    meeting_title = models.CharField('会议名称', max_length=100, null=True)
    meeting_date = models.DateField('会议时间', null=True)
    meeting_area = models.CharField('会议地点', max_length=100, null=True)
    creators = JSONField(verbose_name='作者')
    first_creator = models.CharField('第一作者', max_length=20, null=True, db_index=True)
    organizations = JSONField(verbose_name='作者机构')
    sponsors = JSONField(verbose_name='主办单位', null=True)
    meeting_corpus = models.CharField('母体文献', max_length=100, null=True)
    language = models.CharField('语种', max_length=10, default='中文')
    classifications = JSONField(verbose_name='机标分类号', null=True)
    publish_date = models.DateField('出版日期', null=True)
    page = models.CharField('页码', max_length=20, null=True)
    experts = models.ManyToManyField(Expert, related_name='conferences', db_index=True)

    class Meta:
        db_table = 'conferences'


class Patent(AbstractModel):
    original_id = models.CharField('源数据id', max_length=100, null=True, unique=True, db_index=True)
    name = models.CharField('专利名称', max_length=100, db_index=True)
    abstract = models.TextField('专利简介', null=True)
    patent_type = models.CharField('专利类型', max_length=20, null=True)
    patent_code = models.CharField('专利申请号', max_length=50, unique=True, db_index=True)
    application_date = models.DateField('专利申请日期', null=True)
    publication_number = models.CharField('专利公开号', max_length=50, unique=True, db_index=True)
    publication_date = models.DateField('专利公告日期', null=True)
    main_classifications = JSONField(verbose_name='主分类号', null=True)
    classifications = JSONField(verbose_name='分类号', null=True)
    applicants = JSONField(verbose_name='申请人', null=True)
    inventors = JSONField(verbose_name='发明人', null=True)
    applicant_address = models.CharField('主发明人地址', max_length=200, null=True)
    claim = models.TextField('主权项', null=True)
    region_code = models.CharField('国别省市代码', max_length=20, null=True)
    legal_status = models.CharField('法律状态', max_length=10, null=True)
    experts = models.ManyToManyField(Expert, related_name='patents', db_index=True)

    class Meta:
        db_table = 'patents'


class Periodical(AbstractModel):
    original_id = models.CharField('源数据id', max_length=100, null=True, unique=True, db_index=True)
    title = models.CharField('期刊标题', max_length=100, db_index=True)
    doi = models.CharField('doi', max_length=100, null=True, db_index=True)
    abstract = models.TextField('期刊简介', null=True)
    publish_date = models.DateField('发布日期', null=True)
    keywords = JSONField(verbose_name='关键词', null=True)
    creators = JSONField(verbose_name='作者')
    first_creator = models.CharField('第一作者', max_length=30, null=True)
    organizations = JSONField(verbose_name='作者机构')
    periodical_name = models.CharField('期刊名称', max_length=100, null=True)
    periodical_number = models.CharField('卷', max_length=30, null=True)
    periodical_column = models.CharField('栏目', max_length=50, null=True)
    page_numbers = models.CharField('页码', max_length=20, null=True)
    page_count = models.CharField('总页数', max_length=20, null=True)
    foundations = JSONField(verbose_name='基金项目', null=True)
    classification = JSONField(verbose_name='分类号', null=True)
    experts = models.ManyToManyField(Expert, related_name='periodicals', db_index=True)

    class Meta:
        db_table = 'periodicals'


class Achievement(AbstractModel):
    original_id = models.CharField('源数据id', max_length=100, null=True, unique=True, db_index=True)
    sn = models.CharField('项目年度编号', max_length=100, null=True, db_index=True)
    title = models.CharField('标题', max_length=100, db_index=True)
    organizations = JSONField(verbose_name='完成单位', null=True)
    creators = JSONField(verbose_name='完成人', null=True)
    published_year = models.CharField('公布年份', max_length=20, null=True)
    category = models.CharField('中图分类', max_length=40, null=True)
    keywords = JSONField(verbose_name='关键词', null=True)
    abstract = models.TextField('简介', null=True)
    province = models.CharField('省市', max_length=20, null=True)
    trade_name = JSONField(verbose_name='应用行业名称', null=True)
    level = models.CharField('成果水平', max_length=20, null=True)
    contact_unit = models.CharField('联系单位', max_length=200, null=True)
    contact_address = models.CharField('联系单位地址', max_length=200, null=True)
    experts = models.ManyToManyField(Expert, related_name='achievements', db_index=True)

    class Meta:
        db_table = 'achievements'
