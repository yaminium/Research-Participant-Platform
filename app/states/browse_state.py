import reflex as rx
from app.models import Study
from app.states.auth_state import AuthState
from app.states.study_state import StudyState


class BrowseState(rx.State):
    search_query: str = ""
    filter_compensation: str = ""
    filter_health_type: str = "All"
    filter_experiment_type: str = "All"
    filter_location_type: str = "All"
    filter_duration: str = ""
    current_page: int = 1
    items_per_page: int = 10

    @rx.var(cache=True)
    async def filtered_studies(self) -> list[Study]:
        study_state = await self.get_state(StudyState)
        studies = [s for s in study_state.studies if s["status"] == "Open"]
        if self.search_query:
            query = self.search_query.lower()
            studies = [
                s
                for s in studies
                if query in s["title"].lower() or query in s["description"].lower()
            ]
        if self.filter_compensation:
            comp_query = self.filter_compensation.lower()
            studies = [s for s in studies if comp_query in s["compensation"].lower()]
        if self.filter_health_type != "All":
            studies = [
                s
                for s in studies
                if s["psychological_health_type"] == self.filter_health_type
            ]
        if self.filter_experiment_type != "All":
            studies = [
                s
                for s in studies
                if s.get("experiment_type") == self.filter_experiment_type
            ]
        if self.filter_location_type != "All":
            studies = [
                s for s in studies if s["location_type"] == self.filter_location_type
            ]
        if self.filter_duration:
            dur_query = self.filter_duration.lower()
            studies = [s for s in studies if dur_query in s["duration"].lower()]
        return studies

    @rx.var
    async def total_items(self) -> int:
        studies = await self.filtered_studies
        return len(studies)

    @rx.var
    async def total_pages(self) -> int:
        total = await self.total_items
        if total == 0:
            return 1
        return -(-total // self.items_per_page)

    @rx.var
    async def paginated_studies(self) -> list[Study]:
        studies = await self.filtered_studies
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return studies[start:end]

    @rx.var(cache=True)
    async def current_study(self) -> Study | None:
        study_id = self.router.page.params.get("id")
        if not study_id:
            return None
        study_state = await self.get_state(StudyState)
        for s in study_state.studies:
            if s["id"] == study_id:
                return s
        return None

    @rx.var(cache=True)
    async def current_study_researcher_name(self) -> str:
        study = await self.current_study
        if not study:
            return "Unknown"
        auth_state = await self.get_state(AuthState)
        for u in auth_state.users:
            if u["id"] == study["researcher_id"]:
                return u["name"]
        return "Unknown Researcher"

    @rx.event
    def set_search_query(self, value: str):
        self.search_query = value
        self.current_page = 1

    @rx.event
    def set_filter_health_type(self, value: str):
        self.filter_health_type = value
        self.current_page = 1

    @rx.event
    def set_filter_experiment_type(self, value: str):
        self.filter_experiment_type = value
        self.current_page = 1

    @rx.event
    def set_filter_location_type(self, value: str):
        self.filter_location_type = value
        self.current_page = 1

    @rx.event
    def set_filter_compensation(self, value: str):
        self.filter_compensation = value
        self.current_page = 1

    @rx.event
    def set_filter_duration(self, value: str):
        self.filter_duration = value
        self.current_page = 1

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    @rx.event
    async def next_page(self):
        pages = await self.total_pages
        if self.current_page < pages:
            self.current_page += 1