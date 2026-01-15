from flask import Flask, render_template, abort
from engine.scoring import Scorer

def create_app(scorer: Scorer):
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template(
            "index.html",
            total_points=scorer.total_points,
            stats=scorer.service_stats
        )

    @app.route("/service/<name>")
    def service_detail(name):
        history = [
            r for r in scorer.history
            if r.name == name
        ]

        if not history:
            abort(404)

        return render_template(
            "service.html",
            service_name=name,
            history=history[-20:]
        )

    return app
