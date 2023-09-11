import boto3
import pandas as pd
import io
import logging
from dotenv import load_dotenv
from botocore.exceptions import ClientError
import os

load_dotenv()


class ControllerS3Bucket:
    def __init__(self):
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(os.getenv("BUCKETNAME"))
        self.client = boto3.client('s3')
        self.bucketname = os.getenv("BUCKETNAME")
        self.bucketname_asset = os.getenv("BUCKETNAME_ASSET")

    def file_exists(self, path):
        try:
            self.client.head_object(Bucket=self.bucketname, Key=path)
        except ClientError as e:
            # return int(e.response['Error']['Code']) != 404
            logging.error(e)
            return False
        return True
    
    def get_txt(self, project_id: str, path: str):
        """Returns text string from .txt file in S3."""

        obj = self.bucket.Object(key=project_id + '/' + path)
        response = obj.get()

        txt = response['Body'].read().decode('utf-8')

        return txt

    def save_pandas_to_csv(
            self,
            project_id: str,
            file: str,
            df: pd.DataFrame):
        """ Write a dataframe to a CSV on S3 """
        print("Writing {} records to {}/{}".format(
            len(df),
            project_id, file)
            )
        # Create buffer
        csv_buffer = io.StringIO()
        # Write dataframe to buffer
        df.to_csv(
                csv_buffer,
                sep=";",
                index=False,
                encoding='utf-8-sig',
                decimal=','
                )
        # Create S3 object

        # Write buffer to S3 object
        self.s3.Object(self.bucketname, project_id + '/' + file).put(
                Body=csv_buffer.getvalue().encode('utf-8-sig'))

    def get_csv_to_pandas(self, project_id: str, path: str):
        """Returns DataFrame from csv in S3."""

        obj = self.bucket.Object(key=project_id + '/' + path)
        response = obj.get()

        df = pd.read_csv(
                response.get("Body"),
                encoding='utf-8-sig',
                delimiter=';',
                decimal=','
                )

        return df

    def save_pandas_to_excel(
            self,
            project_id: str, 
            file: str,
            sheet_name: str,
            df: pd.DataFrame
            ):
        """Writes a dataframe to Excel on S3."""
        print(f'Writing {len(df)} records to {project_id}/{file}')

        try:
            # Buscamos archivo en ruta de S3 y le agregamos una hoja
            obj = self.bucket.Object(key=project_id + '/' + file)
            response = obj.get()
            xlsx_buffer = io.BytesIO(response.get('Body').read())

            with pd.ExcelWriter(
                    xlsx_buffer,
                    engine='openpyxl',
                    mode='a',
                    if_sheet_exists='replace'
                    ) as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        except ClientError as ex:

            # Si no encuentra un archivo con ese nombre en S3 entonces se crea uno
            if ex.response['Error']['Code'] == 'NoSuchKey':
                print(f'Se crea archivo excel: {project_id}/{file} dentro del Bucket: {self.bucketname}')

                xlsx_buffer = io.BytesIO()
                with pd.ExcelWriter(
                        xlsx_buffer,
                        engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Write buffer to S3 object
        self.s3.Object(
                self.bucketname, project_id + '/' + file).put(
                Body=xlsx_buffer.getvalue()
                )

    def get_excel_to_pandas(self, project_id: str, path:str, sheet_name:str):

        obj = self.bucket.Object(key=project_id + '/' + path)
        response = obj.get()

        df = pd.read_excel(response.get("Body").read(), sheet_name=sheet_name)

        return df

    def upload_file(self, file_name,asset=False, object_name=None, file_type=''):
        """Upload a file to an S3 bucket

        Parameters:
        file_name (str): File to upload.
        asset (bool): If asset=False uses self.bucketname, otherwhise uses self.bucketname_asset
        object_name (str): S3 object name. If not specified then file_name is used.

        Returns:
        True if file was uploaded, else False
        """
        if asset == False:
            bucket_name = self.bucketname
        else:
            bucket_name = self.bucketname_asset

        # If s3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        if file_type == '':
            extra_args = {}
        elif file_type == 'pdf':
            extra_args = {'ContentType':'application/pdf'}

        # Upload file
        try:
            self.client.upload_file(
                    file_name, 
                    bucket_name,
                    object_name,
                    ExtraArgs=extra_args
                    )
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def get_object(self, filename):
        return self.client.get_object(Bucket=self.bucketname, Key=filename)

