aws s3 mb s3://fcchal1
echo "This is from the challange" >> ./lil3.txt
aws s3 sync ./ s3://fcchal1
aws s3 ls s3://fcchal1

