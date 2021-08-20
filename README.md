# pib

#### 2021
[![PIB_India_Dec_2021](https://github.com/nit-in/pib/actions/workflows/pib_dec_2021.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2021_Dec)
[![PIB_India_Nov_2021](https://github.com/nit-in/pib/actions/workflows/pib_nov_2021.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2021_Nov)
[![PIB_India_Oct_2021](https://github.com/nit-in/pib/actions/workflows/pib_oct_2021.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2021_Oct)
[![PIB_India_Sep_2021](https://github.com/nit-in/pib/actions/workflows/pib_sep_2021.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2021_Sep)
[![PIB_India_Aug_2021](https://github.com/nit-in/pib/actions/workflows/pib_aug_2021.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2021_Aug)
[![PIB_India_Jul_2021](https://github.com/nit-in/pib/actions/workflows/pib_jul_2021.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2021_Jul)
[![PIB_India_Jun_2021](https://github.com/nit-in/pib/actions/workflows/pib_jun_2021.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2021_Jun)
[![PIB_India_May_2021](https://github.com/nit-in/pib/actions/workflows/pib_may_2021.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2021_May)
[![PIB_India_Apr_2021](https://github.com/nit-in/pib/actions/workflows/pib_apr_2021.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2021_Apr)
[![PIB_India_Mar_2021](https://github.com/nit-in/pib/actions/workflows/pib_mar_2021.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2021_Mar)
[![PIB_India_Feb_2021](https://github.com/nit-in/pib/actions/workflows/pib_feb_2021.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2021_Feb)
[![PIB_India_Jan_2021](https://github.com/nit-in/pib/actions/workflows/pib_jan_2021.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2021_Jan)

#### 2020
[![PIB_India_Dec_2020](https://github.com/nit-in/pib/actions/workflows/pib_dec_2020.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2020_Dec)
[![PIB_India_Nov_2020](https://github.com/nit-in/pib/actions/workflows/pib_nov_2020.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2020_Nov)
[![PIB_India_Oct_2020](https://github.com/nit-in/pib/actions/workflows/pib_oct_2020.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2020_Oct)
[![PIB_India_Sep_2020](https://github.com/nit-in/pib/actions/workflows/pib_sep_2020.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2020_Sep)
[![PIB_India_Aug_2020](https://github.com/nit-in/pib/actions/workflows/pib_aug_2020.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2020_Aug)
[![PIB_India_Jul_2020](https://github.com/nit-in/pib/actions/workflows/pib_jul_2020.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2020_Jul)
[![PIB_India_Jun_2020](https://github.com/nit-in/pib/actions/workflows/pib_jun_2020.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2020_Jun)
[![PIB_India_May_2020](https://github.com/nit-in/pib/actions/workflows/pib_may_2020.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2020_May)
[![PIB_India_Apr_2020](https://github.com/nit-in/pib/actions/workflows/pib_apr_2020.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2020_Apr)
[![PIB_India_Mar_2020](https://github.com/nit-in/pib/actions/workflows/pib_mar_2020.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2020_Mar)
[![PIB_India_Feb_2020](https://github.com/nit-in/pib/actions/workflows/pib_feb_2020.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2020_Feb)
[![PIB_India_Jan_2020](https://github.com/nit-in/pib/actions/workflows/pib_jan_2020.yml/badge.svg)](https://github.com/nit-in/pib/releases/tag/v2020_Jan)


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
