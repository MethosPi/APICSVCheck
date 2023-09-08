from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Endpoint to upload a CSV file
@app.route('/upload', methods=['POST'])
def upload_csv():
    try:
        file = request.files['file']
        if not file:
            return jsonify({'error': 'No file uploaded'}), 400

        # Read the uploaded CSV file
        data = pd.read_csv(file)

        # Get the column name from the request parameters (optional)
        column_name = request.args.get('column_name')

        # Ottieni i nomi delle colonne
        

        # If column_name is specified, calculate statistics for that column
        if column_name:
            if column_name not in data.columns:
                return jsonify({'error': f'Column "{column_name}" not found in the CSV file'}), 400

            # Calculate statistics for the specified column
            column_mean = float(data[column_name].mean())
            column_median = float(data[column_name].median())
            column_sum = float(data[column_name].sum())
            column_max = float(data[column_name].max())
            column_min = float(data[column_name].min())
        

            result = {
                'mean': column_mean,
                'median': column_median,
                'sum': column_sum,
                'max': column_max,
                'min': column_min
            }
        else:
            column_names = str(data.columns.tolist())
            # Ottieni i tipi di dati delle colonne
            column_types = str(data.dtypes.tolist())
            result = {
                'column_names': column_names,
                'column_types': column_types,
                'mean': data.mean().to_dict(),
                'median': data.median().to_dict(),
                'sum': data.sum().to_dict(),
                'max': data.max().to_dict(),
                'min': data.min().to_dict()
            }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
