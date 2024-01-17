package com.frankmoley.lil.s3;

import java.nio.file.Paths;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import software.amazon.awssdk.auth.credentials.AwsSessionCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.CreateBucketRequest;
import software.amazon.awssdk.services.s3.model.DeleteObjectRequest;
import software.amazon.awssdk.services.s3.model.GetObjectRequest;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;

public class Application {

    private static final Logger LOGGER = LoggerFactory.getLogger(Application.class);
    private static final String AWS_ACCESS_KEY = "AWS_ACCESS_KEY_ID";
    private static final String AWS_SECRET_KEY = "AWS_SECRET_ACCESS_KEY";
    private static final String PRI_BUCKET_NAME = "fpmlil";
    private static final String TRANSIENT_BUCKET_NAME = "fpmlil2";
    private static final String F1 = "lil1.txt";
    private static final String F2 = "lil2.txt";
    private static final String F3 = "lil3.txt";
    private static final String DIR = "/Users/fpmoles/Desktop/s3";
    private static final String DOWN_DIR = "/Users/fpmoles/Desktop/s3alt";

    private final S3Client s3;

    public Application(S3Client s3){
        this.s3 = s3;
    }

    public void createBucket(String name){
        try{
            CreateBucketRequest request = CreateBucketRequest
                    .builder()
                    .bucket(name)
                    .build();
            s3.createBucket(request);
        }catch(Exception e){
            LOGGER.error("error during create bucket", e);
        }
    }

    public void uploadFile(String bucket, String localFile, String localDirectory, String key){
        try{
            PutObjectRequest request = PutObjectRequest.builder().bucket(bucket).key(key).build();
            s3.putObject(request, Paths.get(localDirectory, localFile));
        }catch (Exception e){
            LOGGER.error("error uploading file", e);
        }
    }

    public void downloadFile(String bucket, String localFile, String localDirectory, String key){
        try{
            GetObjectRequest request = GetObjectRequest.builder().bucket(bucket).key(key).build();
            s3.getObject(request, Paths.get(localDirectory, localFile));
        }catch (Exception e){
            LOGGER.error("error downloading file", e);
        }
    }

    public void deleteFile(String bucket, String key){
        try{
            DeleteObjectRequest request = DeleteObjectRequest.builder().bucket(bucket).key(key).build();
            s3.deleteObject(request);
        }catch (Exception e){
            LOGGER.error("error deleting file", e);
        }
    }


    public static void main(String[] args) {
        String accessKey = System.getenv(AWS_ACCESS_KEY);
        String secretKey = System.getenv(AWS_SECRET_KEY);
        AwsSessionCredentials creds = AwsSessionCredentials.create(accessKey, secretKey, "");

        S3Client s3 = S3Client.builder().credentialsProvider(StaticCredentialsProvider.create(creds)).build();
        Application app = new Application(s3);

        app.uploadFile(TRANSIENT_BUCKET_NAME, F1, DIR, F1);
        app.downloadFile(TRANSIENT_BUCKET_NAME, F1, DOWN_DIR, F1);
        app.deleteFile(TRANSIENT_BUCKET_NAME, F1);
    }
}
