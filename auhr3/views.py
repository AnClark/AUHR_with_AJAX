"""
    【重中之重：视图库】
"""

""" ####################################### 【 引 入 必 要 库 】 #######################################"""
from auhr3 import app, db, lm
from flask import render_template, redirect, session, url_for, request, g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask import flash

from auhr3 import models
from .models import Member, Admin
from auhrlib.Querier import MemberQuerier, MemberQuerierById, department_list
from auhrlib.DateConvertForDB import date_string_to_date_object

from .forms import LoginForm, InputBasicInfoForm, KeyWordQueryForm

# import string

#   引入加密验证模块
from auhrlib.PasswordVerifier import sha256_verify

#   用户权限开关
#   指示HR系统是否在高级用户状态下运行。
#   运用高级用户登录，就可以解锁信息录入、信息修改、信息删除等高级功能。否则，只能进行信息查询。
# session['Premium_User_Switch'] = False

""" ####################################### 【 登 录 管 理 部 分 】 #######################################"""

""" ● 指派全局用户名 ●"""
@app.before_request
def before_request():
    # 全局用户名，在用户登录后指派于此，可为生命周期内所有页面共享
    g.user = current_user


"""  ● 从数据库中加载 HR 用户信息 ● """
@lm.user_loader
def load_user(id):
    return models.Admin.query.get(int(id))


"""
★ ● 站点主入口 ● ★
        先判断用户是否已登录。
            若已登录，则直接跳到主菜单页面（目前只编写基本信息管理页面，因此暂定调到基本信息管理的主菜单）
            若未登录，则跳到登录页面
        【友情提示】和Java类似，Python的对象允许先使用后定义！

"""
@app.route('/')
@app.route('/index')
def index():
        # 未登录的情形
        if str(current_user).find("Anonymous") > 0:
            print("***	Not login. Time to login now!")
            return redirect(url_for('login'))
        # 已登录的情形
        else:
            print("***	Loginned with user: " + current_user.username)
            return redirect(url_for('info'))


"""     ● 登录页面 ●   """
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    if g.user is not None and g.user.is_authenticated():
        # 测试期间，登录成功页面暂时指向基本信息管理页面
        return redirect('/info')
    """
    # 初始化登录表单
    form = LoginForm()

    # 编写表单提交后的动作——登录验证程序。
    # 表单提交后，就会触发validation过程，下面的代码就会运行。
    if form.validate_on_submit():

        # 获取用户输入的用户名和密码
        input_username = form.username.data
        input_password = form.password.data

        # 从用户数据表中查询用户信息
        # 访问数据库有两种方式：db.session（会话模式）与model。
        userinfo_loginer = models.Admin.query.filter_by(username=input_username).first()

        # 根据是否查询到相应用户的信息，来判定用户名是否存在
        # 使用查询方法时，若查询不到，会返回空对象；否则为一个专门的查询结果对象
        if userinfo_loginer is None:
            form.username.errors.append("用户名不存在！")  # 直接将错误信息附加到表单验证器的错误列表中
            return render_template('login/login.html', form=form)   # 重新打开登录页面，要求重新登录

        # ===========================  密码验证过程开始  ===========================
        """从数据库中读取sha256加密后的密码字串
            和 PHP 类似，运行查询函数后获取到的对象并不是字符串，而是与资源有关的各种对象。
            操作备忘录：
            ① 执行 session.query(字段对象) 函数后：生成一个list，成员为按照字段筛选后的 SQLAlchemy 数据元组。
            ② 由于我设置了用户名唯一，因此正常情况下，list中只有一个数据元组。
            ③ 元组的第一个元素即为查询而得的密码字串，但这是以SQLAlchemy数据串的方式存储的（字母u开头的字符串）。
                因此，必须使用str()函数，将它转换为字符串，方可得到我们需要的密码字串。
         """
        password_char = db.session.query(models.Admin.password).filter_by(username=str(input_username)).all()[0]    # 从数据库中查询密码字串
        password_char = str(password_char[0])   # 查询到的密码字串以SQLAlchemy数据串形式存储，因此必须得转换
        password_verify_passed = False

        try:
            password_verify_passed = sha256_crypt.verify(input_password, password_char)
        except ValueError:
            flash("系统错误：数据库中的密码未加密！")

        if password_verify_passed:
            pass
        else:
            form.password.errors.append("密码错误！")
            return render_template('login/login.html', form=form)

            # ===========================  密码验证过程结束  ===========================

        #   检测用户级别
        session['Premium_User_Switch'] = db.session.query(models.Admin.isPremiumUser).filter_by(username=input_username).first()[0][0]
        flash("高级用户与否：%s" % session['Premium_User_Switch'])

        #   登录
        # 【警告！】当填入用户数据库中不存在的用户名时，如果不验证并拦截，就会触发异常！
        login_user(user=userinfo_loginer, remember=form.remember_me.data)

        # 登录通过，即进入主页面。
        # 主页面未建立，因此暂时以基本信息管理部分做之
        return redirect(url_for('info'))

    return render_template('login/login.html', form=form)


"""     ● 登出页面 ●   """
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

"""#########################################################################################################"""


"""###################################### 基 本 信 息 管 理 部 分 ##########################################
        整个基本信息管理系统的核心，汇聚于此。
        所有页面都设置了@login_required装饰器，只允许登录后才能访问。
"""

"""   ● 基本信息录入程序之主页 ● """
@app.route('/info')
@login_required
def info():
    user = g.user
    return render_template('info/index.html', user=user, isPremiumUser=session['Premium_User_Switch'])


"""   ● 基本信息录入页面 ● """
@app.route('/info/input', methods=['GET', 'POST'])
@login_required
def info_input():
    user = g.user

    form = InputBasicInfoForm()
    if form.validate_on_submit():

        new_person = Member(
            Name=form.Name.data,
            Gender=form.Gender.data,
            Mobile=form.Mobile.data,
            QQ=form.QQ.data,
            Birthday=form.Birthday.data,
            Grade=form.Grade.data,
            Faculty=form.Faculty.data,
            Class=form.Class.data,
            DormBuild=form.DormBuild.data,
            Department=form.Department.data,
            GroupInDepart=form.GroupInDepart.data,
            Occupation=form.Occupation.data,
            AUID=form.AUID.data,
            ArrivalTime=form.ArrivalTime.data
        )

        db.session.add(new_person)
        db.session.commit()

        flash("成功添加信息：%s" % form.Name.data)

        return render_template('info/input.html', user=user, isPremiumUser=session['Premium_User_Switch'],
                               form=form)


""" ● 查询入口页面 ●
   在入口页面中，可以直接以关键字或部门分类进行查询（没有必要再去做二级页面）
   查询过程直接在页面中借助 JavaScript 进行。
"""
@app.route('/info/query')
@login_required
def info_query():
    user = g.user
    return render_template('info/query.html', user=user, isPremiumUser=session['Premium_User_Switch'],
                           department_list=department_list)


""" ● 查询结果集页面 ● ——采用了 AJAX 黑科技
   查询结果显示在这里。
   点击条目，即可以以页面内弹窗的形式，展示单人信息报表
   在页面内，还可以再以关键字和部门分类进行查询
"""
@app.route('/info/query_result', methods=['GET'])
@login_required
def info_query_result():
    user = g.user

    """AJAX 黑科技，Flask 支持传入URL参数
    用request.args对象，就可以解析URL参数——它是一个字典，键为你指定的参数名"""
    keyword = request.args['key']

    # 执行数据库查询操作
    result_assembly = MemberQuerier(keyword=keyword)
    # 打开页面
    return render_template('info/query_result.html', user=user, isPremiumUser=session['Premium_User_Switch'],
                           result_assembly=result_assembly, keyword=keyword)


""" ● 个人信息查询结果过程 ● ——采用了 AJAX 黑科技
    【【注意！这是一个过程，而不是一个页面！】】
   全程使用JQuery AJAX，能够在不重载整个前端网页的情况下展示数据，提升使用体验。
   前端向后台发出查询请求，后台 jsonify 函数把查询到的结果集传递到前端页面，后由JavaScript编写的程序进行后续处理
   【媒介】
        1.前端至后台：AJAX request form
        2.后台至前端：JSON 字符串，由 JQuery 进行解析
"""
@app.route('/info/query_person', methods=['GET', 'POST'])
@login_required
def info_query_person():
    idx = int(request.form.get('idx', 0))
    result = MemberQuerierById(idx)[0]
    return jsonify(result=result)


""" ● 修改后之个人信息提交过程 ● ——采用了 AJAX 黑科技
    【【注意！这是一个过程，而不是一个页面！】】
   全程使用JQuery AJAX，能够在不重载整个前端网页的情况下提交数据，提升使用体验。

"""
@app.route('/info/submit_modified_person', methods=['GET', 'POST'])
@login_required
def info_submit_modified_person():
    # ==========    总体思路——先删后添    ==========
    # 先获取当前要修改之信息的索引
    idx = int(request.form.get('idx', 0))
    # 根据索引在数据库中进行查询，获得要修改的项目
    member_for_edit = Member.query.get(idx)
    # 将之数据库中删除，以备重新添加
    db.session.delete(member_for_edit)

    print(request.form.get('Birthday'))
    print(request.form.get('ArrivalTime'))

    # 创建一个新记录——借助Model类的构造方法
    # 请注意，新记录的索引必须与修改前的记录相同，否则就不成其为“修改记录”！
    member_for_edit = Member(
        id=member_for_edit.id,      # 注意新记录的索引设置！
        Name=request.form.get('Name', ''),
        Gender=request.form.get('Gender', ''),
        Mobile=request.form.get('Mobile', ''),
        QQ=request.form.get('QQ', ''),
        Grade=request.form.get('Grade', ''),
        Faculty=request.form.get('Faculty', ''),
        Class=request.form.get('Class', ''),
        DormBuild=request.form.get('DormBuild', ''),
        Department=request.form.get('Department', ''),
        GroupInDepart=request.form.get('GroupInDepart', ''),
        Occupation=request.form.get('Occupation', ''),
        AUID=request.form.get('AUID', ''),

        #  由于对象类型限制，日期要单独进行处理
        Birthday=date_string_to_date_object(request.form.get('Birthday')),
        ArrivalTime=date_string_to_date_object(request.form.get('ArrivalTime')),
    )
    # 将新记录添加回数据库中
    # 加入错误处理功能，当处理出错时可以正确响应
    db.session.add(member_for_edit)     # 添加记录
    db.session.commit()     # 提交对数据库的更改
    #except Exception, msg:
    #    return jsonify(result={'OK': False, 'errmsg': msg})
    #else:
    return jsonify(result={'OK': True, 'changed_who': request.form.get('Name', '')})


