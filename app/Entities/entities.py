class User:
	def __init__(self, email, password, points=0, idn=-1):
		self.email = email
		self.password = password
		self.points = points
		self.idn = idn


class Task:
	def __init__(self, uid, name, description, tags, task_type, base_score, target_time, time_bonus_id, repeat_bonus_id, focus_bonus_id, idn=-1):
		self.uid = uid
		self.name = name
		self.description = description
		self.tags = tags
		self.task_type = task_type
		self.base_score = base_score
		self.target_time = target_time
		self.time_bonus_id = time_bonus_id
		self.repeat_bonus_id = repeat_bonus_id
		self.focus_bonus_id = focus_bonus_id
		self.idn = idn


class TaskLogEntry:
	def __init__(self, uid, tid, duration, focus, remarks, repetition=-1, score=None, idn=-1):
		self.uid = uid
		self.tid = tid
		self.duration = duration
		self.focus = focus
		self.repetition = repetition
		self.remarks = remarks
		self.score = score
		self.idn = idn


class TimeBonus:
	def __init__(self, name, tb_type, multiplier, upper_bound, uid, idn=-1):
		self.name = name
		self.tb_type = tb_type
		self.multiplier = multiplier
		self.upper_bound = upper_bound
		self.uid = uid
		self.idn = idn


class RepeatBonus:
	def __init__(self, name, frequency, upper_bound, uid, idn=-1):
		self.name = name
		self.frequency = frequency
		self.upper_bound = upper_bound
		self.uid = uid
		self.idn = idn


class FocusBonus:
	def __init__(self, name, fb_type, lower_bound, distraction_penalty, uid, idn=-1):
		self.name = name
		self.fb_type = fb_type
		self.lower_bound = lower_bound
		self.distraction_penalty = distraction_penalty
		self.uid = uid
		self.idn = idn
