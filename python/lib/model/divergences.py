# example of calculating the js divergence between two mass functions
# forked from https://machinelearningmastery.com/divergence-between-probability-distributions/#:~:text=KL%20divergence%20can%20be%20calculated,of%20the%20event%20in%20P.&text=The%20value%20within%20the%20sum%20is%20the%20divergence%20for%20a%20given%20event.
#HINT:
# # calculate the jensen-shannon distance metric
# from scipy.spatial.distance import jensenshannon
# from numpy import asarray
# # define distributions
# p = asarray([0.10, 0.40, 0.50])
# q = asarray([0.80, 0.15, 0.05])
# # calculate JS(P || Q)
# js_pq = jensenshannon(p, q, base=2)
# print('JS(P || Q) Distance: %.3f' % js_pq)
# # calculate JS(Q || P)
# js_qp = jensenshannon(q, p, base=2)
# print('JS(Q || P) Distance: %.3f' % js_qp)
#
#
from math import log2
from math import sqrt
from numpy import asarray

# calculate the kl divergence
def kl_divergence(p, q):
	return sum(p[i] * log2(p[i]/q[i]) for i in range(len(p)))

# calculate the js divergence
def js_divergence(p, q):
	m = 0.5 * (p + q)
	return 0.5 * kl_divergence(p, m) + 0.5 * kl_divergence(q, m)

if __name__ is "__main__":
	# define distributions
	p = asarray([0.10, 0.40, 0.50])
	q = asarray([0.80, 0.15, 0.05])
	# calculate JS(P || Q)
	js_pq = js_divergence(p, q)
	print('JS(P || Q) divergence: %.3f bits' % js_pq)
	print('JS(P || Q) distance: %.3f' % sqrt(js_pq))
	# calculate JS(Q || P)
	js_qp = js_divergence(q, p)
	print('JS(Q || P) divergence: %.3f bits' % js_qp)
	print('JS(Q || P) distance: %.3f' % sqrt(js_qp))

	# calculate the jensen-shannon distance metric
	from scipy.spatial.distance import jensenshannon
	from numpy import asarray
	# define distributions
	p = asarray([0.10, 0.40, 0.50])
	q = asarray([0.80, 0.15, 0.05])
	# calculate JS(P || Q)
	js_pq = jensenshannon(p, q, base=2)
	print('JS(P || Q) Distance: %.3f' % js_pq)
	# calculate JS(Q || P)
	js_qp = jensenshannon(q, p, base=2)
	print('JS(Q || P) Distance: %.3f' % js_qp)
