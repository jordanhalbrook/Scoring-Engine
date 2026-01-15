"""
Web interface for the scoring engine.

Provides read-only scoreboard and service detail views.
"""
from flask import Flask, render_template, abort
from engine.scoring import Scorer

def create_app(scorer: Scorer):
    """
    Create and configure the Flask application.
    
    Args:
        scorer: Scorer instance to display data from
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)

    @app.route("/")
    def index():
        """Display main scoreboard with total points and service statistics."""
        period_summary = scorer.get_period_summary()
        return render_template(
            "index.html",
            total_points=scorer.total_points,
            stats=scorer.service_stats,
            period_summary=period_summary,
            period_stats=scorer.service_period_stats
        )

    @app.route("/service/<name>")
    def service_detail(name):
        """Display detailed history for a specific service."""
        history = [
            r for r in scorer.history
            if r.name == name
        ]

        if not history:
            abort(404)

        # Get period stats for this service
        service_period_info = scorer.service_period_stats.get(name, {
            "missed_checks": 0,
            "total_checks": 0
        })

        return render_template(
            "service.html",
            service_name=name,
            history=history[-20:],
            period_info=service_period_info
        )

    return app
