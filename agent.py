from flask import *
from database import *
from newcnn import predictcnn


agent=Blueprint('agent',__name__)

@agent.route('/agenthome',methods=['get','post'])
def agenthome():
    return render_template('agenthome.html')


@agent.route('/agent_view_policy')
def agent_view_policy():
    data={}
    q="select * from policy"
    data['res']=select(q)
    return render_template('agent_view_policy.html',data=data)


@agent.route('/agent_request_policy',methods=['get','post'])
def agent_request_policy():
    data={}
    pid=request.args['pid']
    if 'btn' in request.form:
        vnum=request.form['vnum']
        mnum=request.form['mnum']
        enum=request.form['enum']

        q="insert into policyrequest values (null,'%s','%s','%s','%s','%s',curdate(),'pending')"%(session['aid'],pid,vnum,mnum,enum)
        insert(q)
        flash("Request Send Successfully")
        return redirect(url_for("agent.agenthome"))

    return render_template('agent_request_policy.html',data=data)


@agent.route('/agent_view_mypolicyreq')
def agent_view_mypolicyreq():
    data={}
    q="select * from policy inner join policyrequest using (policy_id) where agent_id='%s'"%(session['aid'])
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        prid=request.args['prid'] 
    else:
        action=None
    
    if action=="showstat":
        q="select * from policy inner join policyrequest using (policy_id) where agent_id='%s' and policyrequest_id='%s'"%(session['aid'],prid)
        data['showv']=select(q)

    
    return render_template('agent_view_mypolicyreq.html',data=data)



import uuid
@agent.route('/agent_damage_request',methods=['get','post'])
def agent_damage_request():
    data={}
    q="select * from policy inner join policyrequest using (policy_id)"
    data['preq']=select(q)
    if 'btn' in request.form:
        plid=request.form['plid']
        image=request.files['image']
        path="static/uploads/"+str(uuid.uuid4())+image.filename
        image.save(path)

        q="insert into damagerequest values (null,'%s','%s','%s','NULL',curdate(),'pending')"%(session['aid'],plid,path)
        id=insert(q)
        
        res=predictcnn(path)
        msg="50"
        amount="50000"
        if str(res)=="0":
            msg="10"
            amount="15000"
        elif str(res)=="1":
            msg="30"
            amount="28000"
        data['amount']=True
        print ("sssssssssssssssssssssssssssssssssss",amount)


    return render_template('agent_damage_request.html',data=data,amount=amount)



@agent.route('/agent_view_damagereq')
def agent_view_damagereq():
    data={}
    q="select *,damagerequest.date as date,damagerequest.status as status  from policy inner join policyrequest using (policy_id) inner join damagerequest using (policyrequest_id)  where damagerequest.agent_id='%s'"%(session['aid'])
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        did=request.args['did'] 
    else:
        action=None
    
    if action=="showstat":
        q="select *,damagerequest.date as date,damagerequest.status as status  from policy inner join policyrequest using (policy_id) inner join damagerequest using (policyrequest_id) where damagerequest.agent_id='%s' and damagerequest_id='%s'"%(session['aid'],did)
        data['showv']=select(q)

    
    return render_template('agent_view_damagereq.html',data=data)


@agent.route("/agent_send_complaint",methods=['get','post'])
def agent_send_complaint():
    data={}

    cid=session['aid']

    if 'btn' in request.form:
        comp=request.form['comp']

        q="insert into complaint values(NULL,'%s','%s','pending',curdate())"%(cid,comp)
        insert(q)
        flash("Complaint Added")
        return redirect(url_for("agent.agent_send_complaint"))
    
    q="select * from complaint where agent_id='%s'"%(cid)
    data['res']=select(q)
    return render_template("agent_send_complaint.html",data=data)