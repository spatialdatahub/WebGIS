from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from datasets.models import Dataset

import requests
import owncloud
import os
from cryptography.fernet import Fernet


def load_dataset(request, pk):
    """
    This needs to be fixed to run asynchronously, incase of a very large
    dataset

    Also there needs to be a better way to hide the cryptokey

    This needs to be changed so that it only runs if the url requires authentication
    Working on that now
    """
    # bring in the dataset by pk
    dataset = Dataset.objects.get(pk=pk)
    # the basedir/filepath stuff can probably be done better
    # set base dir
    base_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    # get key from file
    f = base_dir + "/temp_password.txt"
    g = open(f)
    key = g.read().encode("utf-8")
    g.close()
    cipher_end = Fernet(key)

    # this would probably go better with a little loop or something
    bytes_user = dataset.dataset_user.encode("utf-8")
    bytes_password = dataset.dataset_password.encode("utf-8")
    decrypted_user = cipher_end.decrypt(bytes_user).decode("utf-8")
    decrypted_password = cipher_end.decrypt(bytes_password).decode("utf-8")

    # use owncloud stuff, if the owncloud thing is true
    if dataset.owncloud:
        # owncloud, instead of requests.
        oc = owncloud.Client(dataset.owncloud_instance)
        oc.login(decrypted_user, decrypted_password)
        data = oc.get_file_contents(dataset.owncloud_path)
    else:
        data = requests.get(dataset.url,
                            auth=(decrypted_user, decrypted_password)).content

    return HttpResponse(data)


def portal(request):
    '''
    I'm not ready to try and make this filter function ajax yet. That will
    have to wait a bit longer.
    '''
    dataset_list = Dataset.objects.all()
    template_name = "portal.html"

    if "q" in request.GET:
        q = request.GET["q"]
        dataset_list = Dataset.objects.filter(
            Q(title__icontains=q) | Q(author__icontains=q)) 

    return render(request, template_name, {"dataset_list": dataset_list})


def jstests(request):
    dataset_list = Dataset.objects.all()
    template_name = "jstests.html"
    return render(request, template_name, {"dataset_list": dataset_list})
