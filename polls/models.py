from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    class Meta:
        ordering = ["-pub_date"]
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ["votes"]
        verbose_name_plural = "Choises"
    
    def __str__(self):
        return self.choice_text
