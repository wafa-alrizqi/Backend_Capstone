from django.db import models

EMPLOYMENT_TYPE = (
    ('on site', 'on site'),
    ('remote', 'remote')
)
CITIES = (
    ('Riyadh', 'Riyadh'),
    ('Tabuk', 'Tabuk'),
    ('Jeddah', 'Jeddah')
)
CATEGORIES = (
    ('Developer', 'Developer'),
    ('Designer', 'Designer'),
    ('Writer', 'Writer'),
    ('Marketing', 'Marketing'),
    ('Translator', 'Translator'),
    ('Videographer', 'Videographer'),
    ('Accountant', 'Accountant'),
    (' HR manager', 'HR manager')
)
STATUS = (
    ('pending', 'pending'),
    ('accepted', 'accepted'),
    ('completed', 'completed')
)


class Job(models.Model):
    title = models.CharField(max_length=120, null=False, blank=False)
    requirements = models.TextField(blank=False, null=False)
    type = models.CharField(choices=EMPLOYMENT_TYPE, blank=False, null=False, max_length=120)
    Start_date = models.DateField(blank=False, null=False)
    city = models.CharField(choices=CITIES, blank=False, null=False, max_length=120)
    category = models.CharField(choices=CATEGORIES, blank=False, null=False, max_length=120)
    image = models.TextField()
    employer_id = models.ForeignKey('users.Employer', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.title


class JobApplications(models.Model):
    """
    to connect job id with the job seeker who applied to the specified job
    """
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    jobSeeker = models.ForeignKey('users.JobSeeker', on_delete=models.CASCADE)
    status = models.CharField(default='pending', choices=STATUS, max_length=120)

    def __str__(self):
        return str(self.job) + ' ' + str(self.jobSeeker.user.username) + ' ' + str(self.status)

