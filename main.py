<!DOCTYPE html>
<html>
<head>
  <title>Prediction Filter</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: sans-serif;
      padding: 8px;
      margin: 0 auto;
      font-size: 0.8rem;
      max-width: 100%;
      box-sizing: border-box;
    }

    h2 {
      text-align: center;
      margin: 0 0 12px 0;
      font-size: 1rem;
    }

    label {
      display: block;
      margin-top: 6px;
      font-weight: bold;
      font-size: 0.75rem;
    }

    select, input {
      width: 100%;
      padding: 5px;
      font-size: 0.75rem;
      margin-top: 2px;
      box-sizing: border-box;
    }

    button {
      width: 100%;
      margin-top: 12px;
      padding: 6px;
      font-size: 0.8rem;
      background-color: #4CAF50;
      color: white;
      border: none;
      font-weight: bold;
      cursor: pointer;
    }

    button:hover {
      background-color: #45a049;
    }
  </style>
</head>
<body>
  <h2>Search Historical Predictions</h2>
  <form method="POST">

    <label>Sport:</label>
    <select name="sport">
      <option value="">-- Skip Filter --</option>
      {% for item in sports %}
        <option value="{{ item }}">{{ item }}</option>
      {% endfor %}
    </select>

    <label>Type:</label>
    <select name="type">
      <option value="">-- Skip Filter --</option>
      {% for item in types %}
        <option value="{{ item }}">{{ item }}</option>
      {% endfor %}
    </select>

    <label>Platform:</label>
    <select name="platform">
      <option value="">-- Skip Filter --</option>
      {% for item in platforms %}
        <option value="{{ item }}">{{ item }}</option>
      {% endfor %}
    </select>

    <label>Odd:</label>
    <select name="odds">
      <option value="">-- Skip Filter --</option>
      {% for item in odds %}
        <option value="{{ item }}">{{ item }}</option>
      {% endfor %}
    </select>

    <label>Wide Odd Range:</label>
    <select name="wide_range">
      <option value="">-- Skip Filter --</option>
      {% for item in wide_ranges %}
        <option value="{{ item }}">{{ item }}</option>
      {% endfor %}
    </select>

    <label>Narrow Odd Range:</label>
    <select name="narrow_range">
      <option value="">-- Skip Filter --</option>
      {% for item in narrow_ranges %}
        <option value="{{ item }}">{{ item }}</option>
      {% endfor %}
    </select>

    <label>Stake:</label>
    <select name="stake">
      <option value="">-- Skip Filter --</option>
      {% for item in stakes %}
        <option value="{{ item }}">{{ item }}</option>
      {% endfor %}
    </select>

    <label>Bet Return:</label>
    <select name="bet_return">
      <option value="no">No</option>
      <option value="yes">Yes</option>
    </select>

    <button type="submit">Search</button>
  </form>
</body>
</html>
