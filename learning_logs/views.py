from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """The home page for Learning Log"""
    return render(request,'learning_logs/index.html')
    
@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    
    return render(request,'learning_logs/topics.html',context)

@login_required
def topic(request,topic_id):
    """Show a topic page with its entries"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    if topic.owner!= request.user:
        raise Http404
    context = {'topic':topic, 'entries':entries}
    return render(request,'learning_logs/topic.html',context)
    
@login_required    
def new_topic(request):
    """Add a new topic,, handle the form ,, and get, post methods"""
    if request.method != 'POST':
        # no data sumbettid; create a blank form
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
            
    context = {'form':form }
    return render(request, 'learning_logs/new_topic.html', context)
    
@login_required    
def new_entry(request,topic_id):
    """Add new entry to a particular topic"""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # No data submitted; create a blank form
        form = EntryForm()
        
    else:
        # POST data submitted; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                args=[topic_id]))
                
    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)
    
@login_required    
def edit_entry(request,entry_id):
    """Editting an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                args = [topic.id]))
                
    context = {'entry':entry, 'form':form, 'topic': topic}
    return render(request,'learning_logs/edit_entry.html', context)
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
