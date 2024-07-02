# Brief_Scrapping

```
scrapy startproject moviescraper
```
```
scrapy genspider allocine allocine.fr
```
```
playwright install
cd moviescraper/ 
scrapy crawl allocine
scrapy crawl allocine -O myscrapeddata.csv
```


```
# Cree les ressources
terraform init -upgrade
terraform plan -var-file="terraform.tfvars" -out main.tfplan
terraform apply -var-file="terraform.tfvars"

# Supprimer les ressources
terraform plan -destroy -out main.destroy.tfplan
terraform apply main.destroy.tfplan
```