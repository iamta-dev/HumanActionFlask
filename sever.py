# Server Side
from flask import Flask
from flask_restful import Api,Resource,abort,reqparse,marshal_with,fields
from flask_sqlalchemy import SQLAlchemy,Model
app=Flask(__name__)

# Database config
db=SQLAlchemy(app)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
api=Api(app)

class HumanActionModel(db.Model):
    __tablename__ = 'HumanAction'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    dateTime=db.Column(db.String(100),nullable=False)
    face=db.Column(db.String(100),nullable=False)
    face_acc=db.Column(db.String(100),nullable=False)
    action=db.Column(db.String(100),nullable=False)
    action_acc=db.Column(db.String(100),nullable=False)
    position=db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"HumanAction(name={dateTime},face={face},face_acc={face_acc},action={action},action_acc={action_acc},position={position})"

db.create_all()

#Request Parser
add_args=reqparse.RequestParser()
add_args.add_argument("dateTime",type=str,required=True,help="")
add_args.add_argument("face",type=str,required=True,help="")
add_args.add_argument("face_acc",type=str,required=True,help="")
add_args.add_argument("action",type=str,required=True,help="")
add_args.add_argument("action_acc",type=str,required=True,help="")
add_args.add_argument("position",type=str,required=True,help="")

#Update Request Parser
update_args=reqparse.RequestParser()
update_args.add_argument("dateTime",type=str,help="")
update_args.add_argument("face",type=str,help="")
update_args.add_argument("face_acc",type=str,help="")
update_args.add_argument("action",type=str,help="")
update_args.add_argument("action_acc",type=str,required=True,help="")
update_args.add_argument("position",type=str,required=True,help="")

resource_field={
    "id":fields.Integer,
    "dateTime":fields.String,
    "face":fields.String,
    "face_acc":fields.String,
    "action":fields.String,
    "action_acc":fields.String,
    "position":fields.String
}

# Design API
class Task(Resource):
    @marshal_with(resource_field)
    def get(self):
        result=HumanActionModel.query.all()
        if not result:
            abort(404,message="ไม่มีข้อมูล")
        return result 
    
    @marshal_with(resource_field)
    def post(self):
        args=add_args.parse_args()
        # result=HumanActionModel.query.filter_by(dateTime=args["dateTime"]).first()
        # if result:
        #     abort(409,message="ข้อมูลซํ้า")
        obj=HumanActionModel(
            dateTime=args["dateTime"],
            face=args["face"],
            face_acc=args["face_acc"],
            action=args["action"],
            action_acc=args["action_acc"],
            position=args["position"]
            )
        db.session.add(obj)
        db.session.commit()
        return obj,201

class TaskID(Resource):
    @marshal_with(resource_field)
    def get(self,id):
        result=HumanActionModel.query.filter_by(id=id).first()
        if not result:
            abort(404,message="ไม่พบข้อมูล")
        return result
    
    @marshal_with(resource_field)
    def patch(self,id):
        args=update_args.parse_args()
        result=HumanActionModel.query.filter_by(id=id).first()
        if not result:
           abort(404,message="ไม่พบข้อมูล")
        if args["dateTime"]:
            result.dateTime=args["dateTime"] # result.dateTime chonburi => args['dateTime']=ชลบุรี
        if args["face"]:
            result.face=args["face"]
        if args["face_acc"]:
            result.face_acc=args["face_acc"]
        if args["action"]:
            result.action=args["action"]
        if args["action_acc"]:
            result.action_acc=args["action_acc"]
        if args["position"]:
            result.position=args["position"]
        
        db.session.commit()
        return result

    @marshal_with(resource_field)
    def delete(self,id):
        # HumanActionModel.query.filter(HumanActionModel.id == id).delete()
        # db.session.commit()
        result=HumanActionModel.query.filter_by(id=id).first()
        if not result:
           abort(404,message="ไม่พบข้อมูล")
        else:
           db.session.delete(result) 
           db.session.commit()
       

#call
api.add_resource(Task,"/human-action/")
api.add_resource(TaskID,"/human-action/<int:id>")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

## TEST POSTMAN - get Data All
# http://localhost:5000/human-action/
## TEST POSTMAN - search Data
# http://localhost:5000/human-action/1

# output [Body][JSON]

## TEST POSTMAN - add Data
# [POST] http://localhost:5000/human-action/1
# [Body][raw][JSON]
# {
#     "dateTime":"28/01/21 02:46:42",
#     "face":"Natthawat",
#     "face_acc":"96.32%",
#     "action":"sleeping",
#     "action_acc":"84.65%",
#     "position":"345,567,45,789"
# }

## TEST POSTMAN - add Update
# [PATCH] http://localhost:5000/human-action/1
# [Body][raw][JSON]
# {
#     "face":"Narin",
#     "face_acc":"53.32%",
# }

## TEST POSTMAN - add Delete
# [DELETE] http://localhost:5000/human-action/1
# [Body][raw][JSON]
# {
# }