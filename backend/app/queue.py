import threading
import uuid
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional

@dataclass
class Job:
    id: str
    status: str = "queued"  # queued | running | done | failed
    progress: float = 0.0
    error: Optional[str] = None
    result_id: Optional[int] = None
    media_type: str = ""
    filename: str = ""


class JobQueue:
    def __init__(self):
        self.jobs: Dict[str, Job] = {}
        self._queue = []
        self._cv = threading.Condition()
        self._worker = threading.Thread(target=self._run, daemon=True)
        self._worker.start()

    def enqueue(self, fn: Callable[[Job], int], media_type: str, filename: str) -> str:
        job_id = str(uuid.uuid4())
        job = Job(id=job_id, media_type=media_type, filename=filename)
        self.jobs[job_id] = job
        with self._cv:
            self._queue.append((job, fn))
            self._cv.notify()
        return job_id

    def _run(self):
        while True:
            with self._cv:
                while not self._queue:
                    self._cv.wait()
                job, fn = self._queue.pop(0)
            try:
                job.status = "running"
                job.progress = 0.1
                result_id = fn(job)  # fn should update progress
                job.result_id = result_id
                job.progress = 1.0
                job.status = "done"
            except Exception as e:
                job.status = "failed"
                job.error = str(e)

    def get(self, job_id: str) -> Optional[Job]:
        return self.jobs.get(job_id)


job_queue = JobQueue()
