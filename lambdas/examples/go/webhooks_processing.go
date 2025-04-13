package main

import (
    "context"
    "github.com/aws/aws-lambda-go/lambda"
    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/service/s3"
    "github.com/aws/aws-sdk-go-v2/feature/s3/manager"
)

type Event struct {
    Body string `json:"body"`
}

func HandleRequest(ctx context.Context, event Event) (string, error) {
    cfg, _ := config.LoadDefaultConfig(ctx)
    client := s3.NewFromConfig(cfg)
    uploader := manager.NewUploader(client)
    _, err := uploader.Upload(ctx, &s3.PutObjectInput{
        Bucket: aws.String("webhook-bucket"),
        Key:    aws.String("data.txt"),
        Body:   strings.NewReader(event.Body),
    })
    if err != nil {
        return "", err
    }
    return "Success", nil
}

func main() {
    lambda.Start(HandleRequest)
}

