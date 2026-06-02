import sys
from flask import Flask, render_template_string, request

app = Flask(__name__)

SHARED_STYLES = """
<style>
    body {
        background-color: #121214;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        margin: 0;
        padding: 40px;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 90vh;
    }
    .card {
        background-color: #1a1a1e;
        border: 1px solid #2e2e34;
        border-radius: 12px;
        padding: 32px;
        max-width: 550px;
        width: 100%;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #2e2e34;
        padding-bottom: 16px;
        margin-bottom: 24px;
    }
    h1 {
        font-size: 22px;
        font-weight: 600;
        margin: 0;
        color: #ffffff;
    }
    .status-container {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #1f2937;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }
    .pulse {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    p {
        color: #94a3b8;
        line-height: 1.6;
        font-size: 14px;
    }
    .instruction-step {
        background-color: #1f2937;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 16px;
        border-left: 4px solid #2563eb;
    }
    .form-group {
        margin-bottom: 16px;
        text-align: left;
    }
    label {
        display: block;
        font-size: 13px;
        color: #94a3b8;
        margin-bottom: 6px;
        font-weight: 500;
    }
    input {
        width: 100%;
        padding: 10px;
        background-color: #121214;
        border: 1px solid #2e2e34;
        border-radius: 6px;
        color: white;
        font-size: 14px;
        box-sizing: border-box;
    }
    input:focus {
        outline: none;
        border-color: #2563eb;
    }
    .btn {
        display: block;
        width: 100%;
        background-color: #2563eb;
        color: white;
        text-align: center;
        padding: 12px;
        border-radius: 6px;
        font-weight: 500;
        text-decoration: none;
        margin-top: 24px;
        transition: background-color 0.2s;
        border: none;
        cursor: pointer;
        font-size: 15px;
    }
    .btn:hover {
        background-color: #1d4ed8;
    }
    .matrix-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 16px;
        margin-bottom: 20px;
    }
    .matrix-table th, .matrix-table td {
        padding: 10px;
        text-align: left;
        border-bottom: 1px solid #2e2e34;
        font-size: 14px;
    }
    .matrix-table th {
        color: #94a3b8;
        font-weight: 500;
    }
    .matrix-table td {
        color: #ffffff;
    }
    .total-highlight {
        font-size: 24px;
        font-weight: 700;
        color: #10b981;
        background-color: #142820;
        padding: 16px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #10b981;
        margin-top: 16px;
    }
    .btn-back {
        display: inline-block;
        color: #94a3b8;
        text-decoration: none;
        font-size: 14px;
        margin-top: 20px;
    }
    .btn-back:hover {
        color: #ffffff;
    }
</style>
"""

HOMEPAGE_HTML = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Micromoves Production Dashboard</title>
    {SHARED_STYLES}
</head>
<body>
    <div class="card">
        <div class="header">
            <h1>Micromoves Cloud Dashboard</h1>
            <div class="status-container">
                <div class="pulse"></div>
                <span>Live Engine</span>
            </div>
        </div>
        
        <div class="instruction-step">
            <p style="margin: 0; color: #ffffff; font-weight: 500;">📋 Instructions to get your pricing estimate:</p>
            <p style="margin: 4px 0 0 0; font-size: 13px;">Enter your move parameters below. Our Dynamic Pricing Engine API will instantly calculate the resource cost breakdown and provide your final quote.</p>
        </div>

        <form action="/quote" method="get">
            <div class="form-group">
                <label>Distance (miles):</label>
                <input type="number" name="distance" value="50" min="1" required>
            </div>
            <div class="form-group">
                <label>Crew Size (number of movers):</label>
                <input type="number" name="crew" value="3" min="1" required>
            </div>
            <div class="form-group">
                <label>Demand Multiplier (e.g., 1.0 standard, 1.2 for peak hours):</label>
                <input type="number" step="0.1" name="demand" value="1.2" min="0.5" required>
            </div>
            <button type="submit" class="btn">Calculate Automatic Pricing &rarr;</button>
        </form>
    </div>
</body>
</html>
"""

PRICING_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Micromoves Dynamic Quote</title>
    {shared_styles}
</head>
<body>
    <div class="card">
        <div class="header">
            <h1>📊 Dynamic Pricing Calculation</h1>
            <div class="status-container" style="background: #142820; color: #10b981;">
                <span>Success</span>
            </div>
        </div>

        <p>Your calculated quote details from the Flask API engine using your input values:</p>

        <table class="matrix-table">
            <thead>
                <tr>
                    <th>Pricing Element</th>
                    <th>Rate Matrix Base</th>
                    <th>Calculated Surcharge</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Base Booking Fee</td>
                    <td>Flat Rate</td>
                    <td>$95.00</td>
                </tr>
                <tr>
                    <td>Distance Surcharge</td>
                    <td>{distance:.1f} miles &times; $2.50/mi</td>
                    <td>${distance_cost:.2f}</td>
                </tr>
                <tr>
                    <td>Labor Allocation Surcharge</td>
                    <td>{crew} crew members &times; $40.00</td>
                    <td>${crew_cost:.2f}</td>
                </tr>
                <tr>
                    <td>Demand Adjustment</td>
                    <td>Factor Surcharge</td>
                    <td>&times; {demand}</td>
                </tr>
            </tbody>
        </table>

        <div class="instruction-step" style="border-left-color: #10b981; margin-top: 20px;">
            <p style="margin: 0; color: #ffffff; font-weight: 500;">💡 How we got this estimate:</p>
            <p style="margin: 4px 0 0 0; font-size: 13px;">
                Formula: (Base Booking Fee [<strong>$95.00</strong>] + Distance Cost [<strong>${distance_cost:.2f}</strong>] + Labor Cost [<strong>${crew_cost:.2f}</strong>]) &times; Demand Multiplier [<strong>{demand}</strong>].
            </p>
        </div>

        <div class="total-highlight" style="background-color: #142820; color: #10b981; border: 1px solid #10b981;">
            Total Quote: ${total_estimate:.2f}
        </div>

        <a href="/" class="btn-back">&larr; Return to Form Inputs</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOMEPAGE_HTML)

@app.route('/quote', methods=['GET'])
def quote():
    try:
        distance = float(request.args.get('distance', 50))
        crew = int(request.args.get('crew', 3))
        demand = float(request.args.get('demand', 1.2))
        
        base_fee = 95.00
        distance_cost = distance * 2.50
        crew_cost = crew * 40.00
        total_estimate = (base_fee + distance_cost + crew_cost) * demand
        
        return render_template_string(
            PRICING_PAGE_HTML.format(
                shared_styles=SHARED_STYLES,
                distance=distance,
                crew=crew,
                demand=demand,
                distance_cost=distance_cost,
                crew_cost=crew_cost,
                total_estimate=total_estimate
            )
        )
    except Exception as e:
        return f"<body style='background:#121214;color:red;font-family:sans-serif;'><h2>Engine Processing Error</h2><p>{str(e)}</p><a href='/'>Go Back</a></body>", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
