# repo-AzureWebsite

This is my Cloud Website project. 

In this document I hope to describe my process and the hiccups that I came across along the way while completing this project.

## Intro
This project is one that I came across while searching for projects that would be a good introduction to some of the capabilities in Azure. I chose Azure due to it being the cloud provider that is used at my current place of employment. This project, "The Cloud Resume Challenge", caught my eye while searching for projects on Reddit. It made sense for me to give it a shot as I felt that it involved many of the tools and languages that are commonly used in the industry at this time. It has also always been an interest of mine to create my own website..

## Creating my Website (HTML/CSS)
The second step(the 1st being to acquire the beginner cert in the CSP of your choosing, more on that later.) of this project was to create a website using HTML and CSS. The website needn't be pretty or that of a front end developer, but I still wanted to make something that looked decent. In the end I settled for a minimilastic design that imitated a sheet of paper. Seeing as this was not the main priority of the project, I completed that and decided I would add more detail at a later date. 

## Static Website (Azure Storage)
After the front end of my website was sufficient in my eyes, I jumped into Azure. On sign-up I was provided the ability to sign-up for a free trial account. With this account I would receive $200 in credit for 30 days and select access to several Azure services. With the new trial subscription made, I was ready to continue. 

Making the storage account in Azure was simple enough. Search storage account > click create near the top left > then fill in the details. 
- Select your region
- Select your subscription. Create a resource group under that subscription to assign this new storage account to, if you hadn't created one already.
- Name
etc. 
Most of the options I could leave as default as many things weren't needed due to this being an test project. I did however make sure to change redundancy to local, as I didn't need strong failover options. Again, this was just a test project.

Once the storage account was deployed and the resource went to, I clicked the 'static website' option on the left side of the screen. There I enabled the feature and added 'index.html' to index document name. After saving those changes(and taking note of the primary endpoint url provided), I could then go to 'Containers' on the left hand side and see a new container named $web. Within $web, I can upload the website files that I had created, and.. voilà. I could type the primary endpoint url into my searchbar and gain access to my site.

## Enabling HTTPS, Registering a custom domain name, and Azure DNS (Azure CDN, DNS)
After creating and testing the static website, it was now time for me to utilize a custom domain name and enable https. To begin, I needed to create an Azure CDN(content delivery network) profile. While creating the profile, I created the CDN profile name as well as the CDN endpoint name. For origin type I selected custom origin and provided the primary endpoint that I was given earlier as the origin hostname. Hint: When putting in that url, ensure that you're not adding the scheme(ie: https://) or any forward slashes at the end (/). After this was complete, I was able to visit my static site from the {cdn-endpoint-name}.azureedge.net. 

Problems. Once my CDN endpoint was completed and tested successfully, it was now time for me to create a custom domain. It seemed easy enough, as per Microsoft's documentation I can search for App Service Domains, and once there register a domain for $12. First problem that I ran into was that I was trying to register for a domain that used .in. The wizard said that the domain was available, I entered my contact information for ICANN, questioned why my auto renewal option was greyed out, and enabled privacy protection. Who wouldn't want privacy protection, right? Well, after that was all setup how I wanted, I went to review and create..

.... Error. 

Long story short. I spent at least an hour trying to figure out what was causing issues, come to find out. .in is not supported under Privacy Protection. Bummer, but oh well. This is a temporary project and website I suppose. Fixed all that, went with a basic .com, figured that'd give the least amount of issues, and confirmed it was compatible with privacy protection.

.... Error.

Another error. "Resource cannot be created because the subscription doesn't have a sufficient payment history. Refer to docs for more info." Alright.. So I need to have made payments apparently to purchase this domain through Azure. Alright, but seems a bit silly. After some research, it looks like I can just add my card to my account and they should be able to charge that. No dice. Ok. More research.... People across the internet seem to be saying you need to utilize a pay-as-you go subscription. Alright. Easy Peasy. I can go to subscriptions > find my subscription that I'm using > go to overview > then near the top left I can upgrade subscription. Not a big deal. 

.... Still Error.

Ok. How about I just create a new subscription and see if I can register the custom domain on the newly created one. Nope. At this point, it's been a few days of researching the error, and I'm stuck. So I do what a lot of people suggest for this problem, I contact support. However, after not hearing back from them, I just decided to take my domain purchasing elsewhere. Saw recommendations for porkbun and went with them. Extremely easy to register, and it turned out to be cheaper too! $6.50 vs $11.99. Nice! 

So... after all that fun. Back to business. Once I got my new domain name registered, I went back to the CDN endpoint that I had created earlier and clicked the +Custom Domain option under overview. There I was able to input my new domain name. Once deployed, I selected my newly listed custom domain shown in CDN endpoints, and enabled custom domain HTTPS with CDN managed certificate. This would take a while(as they state), and once once complete would provide my site with HTTPS connectivity and a valid cert. Afterwards, a DNS Zone is created and DNS name servers are generated which will be copied over to your domain provider so that Azure can host the custom domain.

## Visitor Counter
The next part of this project involves adding a counter to my web page that will iterate for each time the site page is visited. This was done using Javascript to call a API created with Azure Functions that communicates with a database that stores the records of visits. 

## Visitor Counter, Part I - Database (CosmosDB)
The first part of this visitor counter involves selecting a database resource to use in Azure. I used CosmoDB Serverless Capacity mode for this, as it would limit the costs. As Microsoft Documentation says, "Azure Cosmos DB serverless best fits scenarios where you expect intermittent and unpredictable traffic with long idle times." Perfect use-case for this project, and since the data I'm storing is not complex, Table API was used. The configuration wizard contains a lot of options, but for my purposes, everything was left the same except for setting backup storage redundancy to local. Once deployed, I went to my new CosmoDB resource > Data Explorer > then created a new table that I would be using for my API. 

## Visitor Counter, Part II - Serverless and APIs (Azure Function, Python, Javascript)
The Azure Function with a HTTPTrigger is what I would be using to connect the CosmosDB with my website. To begin, you will need to create a Function App. Function Apps are used to logically group Functions. With Function Apps, you can choose your runtime stack and the version. I chose Python for reasons discussed in the Intro. When you create your function App, you must also select the OS that it will run on. You have two choices: Linux, and Windows. With using a Python runtime stack however, you are only allowed Linux as a choice. Once that has been created, you can go to the new Function App created, click Functions on the left side of the screen and click create. Unfortunately for me.. this can not be done in Azure Portal and instead recommended Visual Studio Code and provided steps on how to get started. 

Noteworthy things about Visual Studio Code and programming the Azure Function
- When using Visual Studio Code, the Azure Functions extension helps provide a beginning template that you can use. You will also be given a deploy to Function App option that will allow you to upload to your function app created earlier.
- For local testing you will use function.json.
- Cross-Origin Resource Sharing (CORS) allows JavaScript code running in a browser on an external host to interact with your backend. Will need to be enabled for your custom domain name in your Azure Function App once ready.
- Added connection string to Function App-Configurations. This will be setting your environmental variable which you can call with os.environ to connect to your database.

## Building CI/CD pipeline (Github Actions)
Seperated into 3 parts: 
- Frontend workflow
- Backend workflow
- Unit testing

Each workflow will be used to automatically deploy those respective parts of the project if new code is pushed, as well as automatically purge the CDN endpoint so visitors to the website are provided the latest content.  Unit testing will be used to test the functionality of the Azure Function.

For the most part, this was relatively simple. The guidelines in the link below provided a easy template to use, and the main thing to be wary of was replacing the placeholders with the correct values and directories.

https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-static-site-github-actions?tabs=userlevel

## Back to step 1
 And finally, going back to step 1 of this project, I took and passed the AZ-900 course. :)

## Other Tips and Tricks
- During the project(before CI/CD), if you've made changes to your static website on your storage account but are not seeing changes, you may want to purge the cachce on your CDN endpoint. This will reset the cache in your CDN edge nodes, allowing acces to your latest assets.
- Cost Management + Billing - This service will help you analyze the costs of your workloads, make predicitions on your costs, and setup alerts for things you'd like to be made aware.
- Try not to accidently upload secrets to a public location. ie: Github repo. Github Guardian will alert you, but it may be a bit of a pain to resolve.

## TO DO:

- [ ] Implement Terraform.
  