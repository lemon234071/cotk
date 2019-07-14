r"""
``cotk.metrics`` provides classes and functions evaluating results of models.
It provides a fair metric for every model.
"""
from .._utils.unordered_hash import UnorderedSha256
from .._utils.imports import DummyObject
from .._utils.metaclass import LoadClassInterface, DocStringInheritor

class MetricBase(LoadClassInterface, metaclass=DocStringInheritor):
	'''Base class for metrics.
	'''

	DATALOADER_ARGUMENTS = \
		r"""dataloader (:class:`.dataloader.LanguageProcessingBase`): A language generation dataloader."""
	REFERENCE_ALLVOCABS_KEY_ARGUMENTS = \
		r"""reference_allvocabs_key (str):
			The key of reference sentences. Default: ``ref_allvocabs``."""
	FORWARD_REFERENCE_ALLVOCABS_ARGUMENTS = \
				r"""* **data[reference_allvocabs_key]** (list or :class:`numpy.ndarray`):
				  A 2-d jagged or padded array of int. Reference sentences with
				  :ref:`allvocabs <vocab_ref>` in index form.
				  Contains start token (eg: ``<go>``) and end token (eg: ``<eos>``).
				  Size: ``[batch_size, ~ref_sentence_length]``,
				  where "~" means different sizes in this dimension is allowed."""
	FORWARD_REFERENCE_ALLVOCABS_ARGUMENTS_WITH_TORCH = \
		FORWARD_REFERENCE_ALLVOCABS_ARGUMENTS.replace("list or :class:`numpy.ndarray`", \
			"list or :class:`numpy.ndarray` or :class:`torch.Tensor`")
	FORWARD_POST_ALLVOCABS_ARGUMENTS = \
		FORWARD_REFERENCE_ALLVOCABS_ARGUMENTS.replace("reference_allvocabs_key", \
			"post_allvocabs_key")
	FORWARD_RESP_ALLVOCABS_ARGUMENTS = \
		FORWARD_REFERENCE_ALLVOCABS_ARGUMENTS.replace("reference_allvocabs_key", \
			"resp_allvocabs_key")

	LABEL_KEY_ARGUMENTS = \
		r"""label_key (str):
			The key of reference sentence labels. Default: ``label``."""
	LABEL_ARGUMENTS = r"""* **data[label_key]** (list or :class:`numpy.ndarray`):
				  A 1-d array of int.
				  Size: ``[batch_size]``,
				  each element refers to label of one sample"""

	PREDICTION_KEY_ARGUMENTS = \
		r"""prediction_key (str):
			The key of reference sentence predictions. Default: ``prediction``."""
	PREDICTION_ARGUMENTS = r"""* **data[prediction_key]** (list or :class:`numpy.ndarray`):
				  A 1-d array of int.
				  Size: ``[batch_size]``,
				  each element refers to prediction for one sample"""

	MULTI_TURN_REFERENCE_ALLVOCABS_KEY_ARGUMENTS = \
		r"""multi_turn_reference_allvocabs_key (str):
			The key of reference sentences. Default: ``multi_turn_ref_allvocabs``."""
	FORWARD_MULTI_TURN_REFERENCE_ALLVOCABS_ARGUMENTS = \
				r"""* **data[multi_turn_reference_allvocabs_key]** (list or :class:`numpy.ndarray`):
				  A 3-d jagged or padded array of int. Multi-turn reference sentences with
				  :ref:`all vocabs <vocab_ref>`. Contains start token (eg: ``<go>``) and
				  end token (eg: ``<eos>``). Size: ``[batch_size, ~turn_length, ~sentence_length]``,
				  where "~" means different sizes in this dimension is allowed."""
	FORWARD_MULTI_TURN_REFERENCE_ALLVOCABS_ARGUMENTS_WITH_TORCH = \
		FORWARD_MULTI_TURN_REFERENCE_ALLVOCABS_ARGUMENTS.replace("list or :class:`numpy.ndarray`", \
			"list or :class:`numpy.ndarray` or :class:`torch.Tensor`")

	REFERENCE_LEN_KEY_ARGUMENTS = \
		r"""reference_len_key (str):
			The key of lengths of reference sentences.
			Default: ``ref_length``."""
	FORWARD_REFERENCE_LEN_ARGUMENTS = \
				r"""* **data[reference_len_key]** (list or :class:`numpy.ndarray`):
				  Length of reference sentences. Contains start token (eg:``<go>``)
				  and end token (eg:``<eos>``). Size: ``[batch_size]``."""

	MULTI_TURN_REFERENCE_LEN_KEY_ARGUMENTS = \
		r"""multi_turn_reference_len_key (str):
			The key of lengths of reference sentences.
			Default: ``multi_turn_ref_length``."""
	FORWARD_MULTI_TURN_REFERENCE_LEN_ARGUMENTS = \
				r"""* **data[multi_turn_reference_len_key]** (list or :class:`numpy.ndarray`):
				  A 2-d jagged or padded array of int. **If padded, redundant position must be set to** ``0``.
				  Length of multi-turn reference sentences. Contains start token (eg:``<go>``)
				  and end token (eg:``<eos>``). Size: ``[batch_size, ~turn_length]``,
				  where "~" means different sizes in this dimension is allowed."""

	GEN_KEY_ARGUMENTS = \
		r"""gen_key (str):
			The key of generated sentences. Default: ``gen``."""
	FORWARD_GEN_ARGUMENTS = \
				r"""* **data[gen_key]** (list or :class:`numpy.ndarray`):
				  A 2-d jagged or padded array of int.
				  Sentences generated by model. Contains end token (eg: ``<eos>``),
				  but without start token (eg: ``<go>``).
				  Size: ``[batch_size, ~gen_sentence_length]``,
				  where "~" means different sizes in this dimension is allowed."""

	MULTI_TURN_GEN_KEY_ARGUMENTS = \
		r"""multi_turn_gen_key (str):
			The key of generated sentences. Default: ``multi_turn_gen``."""
	FORWARD_MULTI_TURN_GEN_ARGUMENTS = \
				r"""* **data[gen_key]** (list or :class:`numpy.ndarray`):
				  A 3-d jagged or padded array of int. Sentences generated by model.
				  Contains end token (eg: ``<eos>``), but without start token (eg: ``<go>``).
				  Size: ``[batch_size, ~max_turn_length, ~gen_sentence_length]``,
				  where "~" means different sizes in this dimension is allowed."""

	MULTI_TURN_LENGTH_KEY_ARGUMENTS = \
		r"""turn_length (str):
			The key of length of turns. Default: ``turn_length``."""
	FORWARD_MULTI_TURN_LENGTH_ARGUMENTS = \
				r"""* **data[turn_len_key]** (list or :class:`numpy.ndarray`):
				  Length of turns in each sample.
				  Size: ``[batch_size]``."""

	CPU_COUNT_ARGUMENTS = \
		r"""cpu_count (int): Number of used cpu for multiprocessing. Multiprocessing will **NOT** be used
			when ``cpu_count`` is set to ``1`` or the dataset is small. Default: if ``None``,
			the environment variable ``CPU_COUNT`` will be used	when it is set,
			or all available cpu will be used otherwise."""

	def __init__(self):
		self.unordered_hash = UnorderedSha256()
		self.closed = False

	def _hash_relevant_data(self, data_list):
		'''Invoked by :meth:`.forward` or :meth:`.close` to hash relevant data when computing a metric.

		Arguments:
			data_list (list): relevant data organized as list.
		'''
		for item in data_list:
			self.unordered_hash.update_data(repr(item).encode())

	def _hashvalue(self):
		'''Invoked by :meth:`.close` to return the recorded hash value.
		'''
		return self.unordered_hash.digest()

	def forward(self, data):
		'''Processing a batch of data.

		Arguments:
			data (dict): A dict contains the data that metrics need.
		'''
		if self.closed:
			raise ValueError("The metric has been closed.")
		if not isinstance(data, dict):
			raise TypeError("Data must be a dict.")

	def close(self):
		'''
		Close the metric and return results. Once the metric is closed,
		any operation on the metric (e.g. forward or another close) will raise a ValueError.

		Returns:
			(dict) which contains results.
		'''
		if not self.closed:
			self.closed = True
			return {}
		else:
			raise RuntimeError("The metric has been closed.")

class MetricChain(MetricBase):
	'''A metric-like class for stacked metric. You can use this class
	making multiples metric combination like one.

	Examples:
		>>> metric = MetricChain()
		>>> metric.add_metric(BleuCorpusMetric())
		>>> metric.add_metric(SingleDialogRecorder(dataloader))

	Todo: Give more examples to combining forward and close
	'''
	def __init__(self):
		super().__init__()
		self.metric_list = []

	def add_metric(self, metric):
		'''Add metric for processing.

		Arguments:
			metric (MetricBase): a metric class.
		'''
		if not isinstance(metric, MetricBase):
			raise TypeError("Metric must be a subclass of MetricBase")
		self.metric_list.append(metric)

	def forward(self, data):
		'''Processing a batch of data.

		Arguments:
			data (dict): A dict at least contains keys which all the
				metric components need.
		'''
		super().forward(data)
		for metric in self.metric_list:
			metric.forward(data)

	def close(self):
		r'''
		Returns:
			(dict): A dict which contains the items which all the
			metric components returned.
		'''
		res = super().close()
		for metric in self.metric_list:
			res.update(metric.close())
		return res
