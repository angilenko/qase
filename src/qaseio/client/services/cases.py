from typing import Union

from qaseio.client.models import TestCaseCreate, TestCaseUpdate, TestCaseFilters, \
    TestCaseInfo, TestCaseList, TestCaseCreated
from qaseio.client.services import BaseService, NotFoundException


class Cases(BaseService):
    def get_all(
        self,
        code: str,
        limit=None,
        offset=None,
        filters: TestCaseFilters = None,
    ):
        query = {"limit": limit, "offset": offset}
        if filters:
            query.update(filters.filter())
        return self.vr(
            self.s.get(self.path("case/{}".format(code)), params=query),
            to_type=TestCaseList,
        )

    def get(self, code: str, case_id: Union[str, int]):
        return self.vr(
            self.s.get(self.path("case/{}/{}".format(code, case_id))),
            to_type=TestCaseInfo,
        )

    def delete(self, code: str, case_id: Union[str, int]):
        return self.vr(
            self.s.delete(self.path("case/{}/{}".format(code, case_id))),
            to_type=None,
        )

    def exists(self, code: str, case_id: Union[str, int]):
        try:
            return self.get(code, case_id)
        except NotFoundException:
            return False

    def create(self, code: str, data: TestCaseCreate):
        return self.vr(
            self.s.post(self.path("case/{}".format(code)), data=data),
            to_type=TestCaseCreated,
        )

    def update(self, code: str, case_id: str, data: TestCaseUpdate):
        return self.vr(
            self.s.patch(
                self.path("case/{}/{}".format(code, case_id)),
                data=data,
            ),
            to_type=TestCaseCreated,
        )
