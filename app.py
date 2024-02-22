from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

# AWS S3 configuration
S3_ACCESS_KEY = 'AKIAZQ3DP2D7QAMLFOKZ'
S3_SECRET_KEY = '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'

s3 = boto3.client(
    's3',
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY
)

@app.route('/')
def index():
    # List content of S3 bucket
    buckets = s3.list_buckets()['Buckets']
    return render_template('index.html', buckets=buckets)

@app.route('/bucket_contents', methods=['POST'])
def bucket_contents():
    bucket_name = request.form['bucket_name']
    response = s3.list_objects_v2(Bucket=bucket_name)
    contents = [obj['Key'] for obj in response.get('Contents', [])]
    return render_template('bucket_contents.html', bucket_name=bucket_name, contents=contents)

@app.route('/create_bucket', methods=['POST'])
def create_bucket():
    bucket_name = request.form['bucket_name']
    s3.create_bucket(Bucket=bucket_name)
    return '', 204

@app.route('/delete_bucket', methods=['POST'])
def delete_bucket():
    bucket_name = request.form['bucket_name']
    s3.delete_bucket(Bucket=bucket_name)
    return '', 204

@app.route('/create_folder', methods=['POST'])
def create_folder():
    bucket_name = request.form['bucket_name']
    folder_name = request.form['folder_name']
    s3.put_object(Bucket=bucket_name, Key=(folder_name + '/'))
    return '', 204

@app.route('/delete_folder', methods=['POST'])
def delete_folder():
    bucket_name = request.form['bucket_name']
    folder_name = request.form['folder_name']
    s3.delete_object(Bucket=bucket_name, Key=(folder_name + '/'))
    return '', 204

@app.route('/upload_file', methods=['POST'])
def upload_file():
    bucket_name = request.form['bucket_name']
    file = request.files['file']
    s3.upload_fileobj(file, bucket_name, file.filename)
    return '', 204

@app.route('/delete_file', methods=['POST'])
def delete_file():
    bucket_name = request.form['bucket_name']
    file_name = request.form['file_name']
    s3.delete_object(Bucket=bucket_name, Key=file_name)
    return '', 204

@app.route('/move_file', methods=['POST'])
def move_file():
    bucket_name = request.form['bucket_name']
    source_file = request.form['source_file']
    destination_file = request.form['destination_file']
    copy_source = {'Bucket': bucket_name, 'Key': source_file}
    s3.copy_object(CopySource=copy_source, Bucket=bucket_name, Key=destination_file)
    s3.delete_object(Bucket=bucket_name, Key=source_file)
    return '', 204

@app.route('/copy_file', methods=['POST'])
def copy_file():
    bucket_name = request.form['bucket_name']
    source_file = request.form['source_file']
    destination_file = request.form['destination_file']
    copy_source = {'Bucket': bucket_name, 'Key': source_file}
    s3.copy_object(CopySource=copy_source, Bucket=bucket_name, Key=destination_file)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
