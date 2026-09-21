from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from assignments.models import Assignment

from .forms import SubmissionForm
from .models import Submission

@login_required
def create_submission(request, assignment_id):
    if not request.user.is_student:
        raise PermissionDenied

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        is_published=True,
        course__enrollments__student=request.user,
    )

    if Submission.objects.filter(
        student=request.user,
        assignment=assignment,
    ).exists():
        return redirect(
            "assignments:assignment_detail",
            assignment_id=assignment.id,
        )

    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.full_clean()
            submission.save()

            return redirect(
                "submissions:submission_detail",
                submission_id=submission.id,
            )
    else:
        form = SubmissionForm()

    return render(
        request,
        "submissions/create_submission.html",
        {
            "form": form,
            "assignment": assignment,
        },
    )

@login_required
def submission_detail(request, submission_id):
    if not request.user.is_student:
        raise PermissionDenied

    submission = get_object_or_404(
        Submission,
        id=submission_id,
        student=request.user,
    )

    return render(
        request,
        "submissions/submission_detail.html",
        {
            "submission": submission,
            "assignment": submission.assignment,
        },
    )