from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# 暫時將文章存在記憶體中
posts = [
    {
        "id": 1,
        "title": "加拿大米飛探討",
        "author": "小妮",
        "content": "你們說為什麼加拿大沒有專屬米飛?\n真神奇。"
    },
    {
        "id": 2,
        "title": "關於台科阿虎",
        "author": "小緹",
        "content": "為甚麼我一入學和平阿虎就消失了，但台科阿虎沒事?"
    }
]


@app.route("/")
def index():
    # 顯示所有文章
    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    # 根據文章 ID 找出指定文章
    post = next(
        (p for p in posts if p["id"] == post_id),
        None
    )

    if post is None:
        abort(404)

    return render_template("post.html", post=post)


@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        # 取得表單輸入資料
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        content = request.form.get("content", "").strip()

        # 確認欄位都有填寫
        if not title or not author or not content:
            return render_template(
                "new_post.html",
                error="請填寫所有欄位",
                title=title,
                author=author,
                content=content
            ), 400

        # 新增文章
        new_id = max(
            (p["id"] for p in posts),
            default=0
        ) + 1

        posts.append({
            "id": new_id,
            "title": title,
            "author": author,
            "content": content
        })

        return redirect(url_for("show_post", post_id=new_id))

    return render_template("new_post.html")


if __name__ == "__main__":
    app.run(debug=True)