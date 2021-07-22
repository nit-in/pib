# pib

Download articles from [Press Information Bureau, India](https://www.pib.gov.in).
This might be helpful for candidates preparing for different govt examinations.

## How to use:

```shell

#Clone the repo with:
git clone https://github.com/nit-in/pib
#cd to the cloned repo
cd pib
#installing required packages
pip install -r requirements.txt
#when these steps are done,you are ready to run the spider and download the articles.

#source the env file
source .env

#if you are using shell other than bash then 
bash --init-file .env

#run the spider
pib start_date end_date #(date format: yyyy-mm-dd)
#example => to download the articles from June 1st, 2021 to June 15th, 2021; use
pib 2021-06-01 2021-06-15
```

For an Entire Month

```shell
#For the month of Jan, 2021
pib_month Jan 2021

#For the month of Dec, 2020
pib_month Dec 2020
``` 

Any suggestions and improvements are welcome.
