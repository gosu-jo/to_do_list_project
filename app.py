from flask import Flask,render_template,flash,request,redirect
import json
app = Flask(__name__)
app.secret_key = "dev-secret-key"
FILENAME = "to_do_list.json"

def load_json():
    try:
        with open(FILENAME,"r",encoding='utf-8')as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_json(to_do_lists):
    with open(FILENAME,'w',encoding='utf-8')as file:
        return json.dump(to_do_lists,file,ensure_ascii=False,indent=4) 


def to_do_text():
    to_do = request.form['to_do'].strip()
    time = request.form['time'].strip()
    content = request.form['content'].strip()
    if not (to_do and time and content):
        return None
    return to_do,time,content

def is_vaild_index(to_do_lists,index):
    return 0 <= index < len(to_do_lists)
        

@app.route("/")
def home():
    to_do_lists=load_json()
    return render_template("to_do.html",to_do_lists=to_do_lists)

@app.route("/write/")
def write():
    to_do_lists=load_json()
    return render_template("write.html",to_do_lists=to_do_lists)

@app.route("/write/detail/", methods=['POST'])
def write_detail():
    to_do_lists = load_json()
    to_do_list = to_do_text()
    if not to_do_list:
        flash("제목,시간,내용을 빈칸없이 입력해주세요.")
        return redirect("/write/")
    to_do,time,content = to_do_list

    to_do_list = {
        "to_do" : to_do,
        "time" : time,
        "content" : content
    }
    to_do_lists.append(to_do_list)
    save_json(to_do_lists)
    return redirect("/")


@app.route("/delete/<int:index>", methods=['POST'])
def delete_to_do(index):
    to_do_lists=load_json()
    if not (to_do_lists and is_vaild_index(to_do_lists,index)):
        flash("등록된 할일이 없습니다.")
        return redirect("/")

    to_do_lists.pop(index)
    save_json(to_do_lists)
    return redirect("/")

@app.route("/edit/<int:index>", methods=["POST"])
def edit(index):
    to_do_lists=load_json()
    if not (to_do_lists and is_vaild_index(to_do_lists,index)):
        flash("등록된 할일이 없습니다.")
        return redirect("/")
    to_do_list = to_do_lists[index]
    return render_template("edit.html",to_do_list=to_do_list,index=index)


@app.route("/write/update/<int:index>", methods=['POST'])
def update(index):
    to_do_lists=load_json()
    if not(to_do_lists and is_vaild_index(to_do_lists,index)):
        flash("수정할 항목이 없습니다.")
        return redirect("/")
    to_do_list=to_do_text()
    if not to_do_list:
        flash("제목,시간,내용을 빈칸없이 전부 입력해주세요.")
        return render_template("edit.html",to_do_list=to_do_list,index=index)
    to_do,time,content = to_do_list
    to_do_list = {
        "to_do" : to_do,
        "time" : time,
        "content" : content
    }
    
    to_do_lists[index] = to_do_list
    save_json(to_do_lists)
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
