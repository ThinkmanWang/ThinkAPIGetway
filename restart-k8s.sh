#!/bin/sh

docker build . -t localhost:32000/think-apigateway:latest
docker push localhost:32000/think-apigateway:latest
kubectl rollout restart -n kube-system deployment think-apigateway
