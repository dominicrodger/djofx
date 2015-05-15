from django.views.generic import TemplateView
from operator import itemgetter
from random import shuffle

from djofx import models
from djofx.utils import get_classifier, get_training_data
from djofx.views.base import PageTitleMixin


class AccuracyView(PageTitleMixin, TemplateView):
    template_name = 'djofx/accuracy.html'
    page_title = 'Classifier Accuracy'

    def get_context_data(self, **kwargs):
        ctx = super(AccuracyView, self).get_context_data(**kwargs)
        training_data = get_training_data(self.request.user)
        classifier = get_classifier(self.request.user, training_data)
        ctx['keywords'] = classifier.informative_features()[:20]

        shuffle(training_data)
        training_size = int(len(training_data) * 0.75)
        training_elements = training_data[:training_size]
        test_elements = training_data[training_size:]

        sample_classifier = get_classifier(self.request.user, training_elements)

        ctx['accuracy'] = sample_classifier.accuracy(test_elements) * 100.0

        samples = []

        for element in test_elements[:30]:
            prob_dist = sample_classifier.prob_classify(element[0])
            entry = {}
            entry["payee"] = element[0]
            entry["result"] = prob_dist.max()
            entry["confidence"] = prob_dist.prob(prob_dist.max()) * 100.0
            entry["actual_result"] = element[1]
            entry["actual_confidence"] = prob_dist.prob(element[1]) * 100.0
            samples.append(entry)

        samples = sorted(samples, key=itemgetter('confidence'), reverse=True)

        ctx["samples"] = samples

        return ctx
