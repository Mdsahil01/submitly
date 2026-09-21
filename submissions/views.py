from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from assignments.models import Assignment

from .forms import SubmissionForm, EvaluationForm
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


@login_required
def assignment_submissions(request, assignment_id):
    """Faculty view to list all submissions for an assignment."""
    if not request.user.is_faculty:
        raise PermissionDenied
    
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        created_by=request.user,
    )
    
    submissions = (
        Submission.objects
        .filter(assignment=assignment)
        .select_related('student')
        .order_by('-submitted_at')
    )
    
    return render(
        request,
        "submissions/assignment_submissions.html",
        {
            "assignment": assignment,
            "submissions": submissions,
        },
    )


@login_required
def faculty_submission_review(request, submission_id):
    """Faculty view to review and evaluate a submission."""
    if not request.user.is_faculty:
        raise PermissionDenied
    
    submission = get_object_or_404(
        Submission.objects.select_related('student', 'assignment', 'assignment__course'),
        id=submission_id,
    )
    
    # Verify faculty owns the assignment
    if submission.assignment.created_by != request.user:
        raise PermissionDenied
    
    if request.method == "POST":
        form = EvaluationForm(
            request.POST,
            instance=submission,
            assignment=submission.assignment
        )
        
        if form.is_valid():
            evaluated_submission = form.save(commit=False)
            
            # Update status to REVIEWED when marks are provided
            if evaluated_submission.marks is not None:
                evaluated_submission.status = Submission.STATUS_REVIEWED
                evaluated_submission.reviewed_at = timezone.now()
            
            evaluated_submission.save()
            
            return redirect(
                "submissions:assignment_submissions",
                assignment_id=submission.assignment.id
            )
    else:
        form = EvaluationForm(
            instance=submission,
            assignment=submission.assignment
        )
    
    return render(
        request,
        "submissions/faculty_submission_review.html",
        {
            "submission": submission,
            "assignment": submission.assignment,
            "form": form,
        },
    )