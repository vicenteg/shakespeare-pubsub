# Publishing/Subscribing Shakespeare to Pub/Sub

This is a simple set of scripts to trivially demonstrate publish/subscribe using Google Cloud Pub/Sub.

This code will read from a Google Cloud Storage bucket, do a little text processing, and 
write messages to Google Cloud Pub/Sub. As the title suggests, we'll (re?)publish a Shakespeare
play to Pub/Sub.

# Pre-requisites

To try this, you'll need to have set up a Google Cloud Platform project. You can take advantage of the [GCP free trial](https://console.cloud.google.com/freetrial) if you like.

You can skip these steps if you're certain Pub/Sub is already ready to use in your project.

Next, run through the [Quickstart: Using the Console](https://cloud.google.com/pubsub/docs/quickstart-console) guide.

# Getting this stuff

```

```

## Set up a compute instance

We will use this instance to work with the code. We won't work locally (on our laptops) during this session to avoid the inevitable "doesn't work for me" scenarios. Set this instance up ahead of time and power it off if you like, but be aware that you may be responsible for a couple days worth of persistent disk charges.

Create a n1-standard-1 instance using the **Ubuntu 16.04 LTS** image in the Cloud Platform UI.

Launch cloud shell. Run the following, substituting your instance's name as needed:

```
gcloud compute ssh instance-1
```
 
You will probably be promted to create an ssh key - follow the prompts. A passphrase for your ssh key is not necessary for this workshop.

Once logged in, update your gcloud components:

```
gcloud components update
```

Then install maven, git and python-(pip|virtualenv):

```
sudo apt-get update
sudo apt-get install python-pip python-virtualenv git
```

Create and source a virtualenv, then install `google-cloud-pubsub` and `google-cloud-storage`:

```
virtualenv ~/.env
source ~/.env/bin/activate
pip install --upgrade google-cloud-pubsub google-cloud-storage
```

Now, get this code from this repository:

```
git clone ...
cd ...
```

Now run the publisher script. This script will read a play (King Lear) from Google Cloud Storage, make a half-hearted attempt to filter out non-speaking lines, and publish each line to Pub/Sub as a JSON object.

On running the script, you'll notice that it fails with an error message something like `StatusCode.PERMISSION_DENIED, Request had insufficient authentication scopes`. That's because you're using a service account without authentication from your compute instance. What you should do is go to the console, and generate a keyfile for your instance's service account.

Navigate to [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) and click the menu on the right hand side, then click "Create key".

Copy this key to your instance. One way to do this is to open the .json file in an editor, and copy/paste it to a new file in your home directory on your instance.
 
Re-run the script, and it should run for a while, and exit silently.
