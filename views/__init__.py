from flask import Blueprint


admin_blu = Blueprint('admin_blu', __name__)
index_blu = Blueprint('index_blu', __name__)
job_blu = Blueprint('job_blu', __name__)
company_blu = Blueprint('company_blu', __name__)
user_blu = Blueprint('user_blu', __name__)

from . import admin
from . import index
from . import job
from . import company
from . import user