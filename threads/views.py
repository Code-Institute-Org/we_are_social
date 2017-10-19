from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.forms import formset_factory
from threads.models import Subject, Post, Thread
from .forms import ThreadForm, PostForm
from polls.forms import PollSubjectForm, PollForm
from polls.models import PollSubject


def forum(request):
    return render(request, 'forum/forum.html',
                  {'subjects': Subject.objects.all()})


def threads(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'forum/threads.html', {'subject': subject})


def save_thread(thread_form, post_form, subject, user):
    thread = thread_form.save(commit=False)
    thread.subject = subject
    thread.user = user
    thread.save()

    post = post_form.save(commit=False)
    post.user = user
    post.thread = thread
    post.save()
    return thread


def save_poll(poll_form, poll_subject_formset, thread):
    poll = poll_form.save(commit=False)
    poll.thread = thread
    poll.save()

    for subject_form in poll_subject_formset:
        subject = subject_form.save(commit=False)
        subject.poll = poll
        subject.save()


@login_required
def new_thread(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    poll_subject_formset_class = formset_factory(PollSubjectForm, extra=3)

    if request.method == "POST":
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST)
        poll_form = PollForm(request.POST)
        poll_subject_formset = poll_subject_formset_class(request.POST)

        is_a_poll = request.POST.get('is_a_poll')
        thread_valid = thread_form.is_valid() and post_form.is_valid()
        poll_valid = poll_form.is_valid() and poll_subject_formset.is_valid()

        if (thread_valid and not is_a_poll):
            thread = save_thread(thread_form, post_form, subject, request.user)
            messages.success(request, "You have created a new thread!")
            return redirect(reverse('thread', args=[thread.pk]))


        if (thread_valid and is_a_poll and poll_valid):
            thread = save_thread(thread_form, post_form, subject, request.user)
            save_poll(poll_form, poll_subject_formset, thread)
            messages.success(
                request, "You have created a new thread with a poll!")
            return redirect(reverse('thread', args=[thread.pk]))

    else:
        thread_form = ThreadForm()
        post_form = PostForm()
        poll_form = PollForm()
        poll_subject_formset = poll_subject_formset_class()

    args = {
        'thread_form': thread_form,
        'post_form': post_form,
        'subject': subject,
        'poll_form': poll_form,
        'poll_subject_formset': poll_subject_formset
    }

    args.update(csrf(request))

    return render(request, 'forum/thread_form.html', args)


def thread(request, thread_id):
    thread_ = get_object_or_404(Thread, pk=thread_id)
    args = {'thread': thread_}
    args.update(csrf(request))
    return render(request, 'forum/thread.html', args)


@login_required
def new_post(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(False)
            post.thread = thread
            post.user = request.user
            post.save()

            messages.success(request,
                             "Your post has been added to the thread!")

            return redirect(reverse('thread', args={thread.pk}))

    else:
        form = PostForm()

    args = {
        'form': form,
        'form_action': reverse('new_post', args={thread.id}),
        'button_text': 'Update Post'
    }

    args.update(csrf(request))

    return render(request, 'forum/post_form.html', args)


@login_required
def edit_post(request, thread_id, post_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "You have updated your thread!")

            return redirect(reverse('thread', args={thread_id}))
    else:
        form = PostForm(instance=post)

    args = {
        'form': form,
        'form_action': reverse('edit_post', kwargs={
                               "thread_id": thread.id, "post_id": post.id}),
        'button_text': 'Update Post'
    }

    args.update(csrf(request))

    return render(request, 'forum/post_form.html', args)


@login_required
def delete_post(request, thread_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()

    messages.success(request, "Your post was deleted!")

    return redirect(reverse('thread', args={thread_id}))


@login_required
def thread_vote(request, thread_id, subject_id):
    thread = Thread.objects.get(id=thread_id)
    subject = thread.poll.votes.filter(user=request.user)

    if subject:
        messages.error(request, "You already voted on this!... "
                                "You're not trying to cheat are you?")
        return redirect(reverse('thread', args={thread_id}))

    subject = PollSubject.objects.get(id=subject_id)
    subject.votes.create(poll=subject.poll, user=request.user)

    messages.success(request, "We've registered your vote!")

    return redirect(reverse('thread', args={thread_id}))
