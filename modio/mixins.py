"""Module storing all mixins for shared methods"""

from .errors import modioException
from .enums import RatingType, Report
from . import entities


class ReportMixin:
    """Mixin for entities that can be reported, requireds 'resource_type' to
    be defined at a class level.
    """

    def _make_report_dict(self, name, summary, report_type):
        return {
            "id": self.id,
            "resource": self.resource_type,
            "name": name,
            "type": report_type.value,
            "summary": summary,
        }

    def report(self, name, summary, report_type=Report(0)):
        """Report a this game, make sure to read mod.io's ToU to understand what is
        and isnt allowed.

        |coro|

        Parameters
        -----------
        name : str
            Name of the report
        summary : str
            Detailed description of your report. Make sure you include all relevant information and
            links to help moderators investigate and respond appropiately.
        report_type : Report
            Report type

        Returns
        --------
        Message
            The returned message on the success of the query.

        """

        msg = self.connection.post_request("/report", data=self._make_report_dict(name, summary, report_type))
        return entities.Message(**msg)

    async def async_report(self, name, summary, report_type=Report(0)):
        msg = await self.connection.async_post_request(
            "/report", data=self._make_report_dict(name, summary, report_type)
        )
        return entities.Message(**msg)


class RatingMixin:
    """Mixin for entities that can be rated, required 'mod_key' to
    be defined.
    """

    def _add_rating(self, rating: RatingType):
        try:
            mod_id = getattr(self, self.mod_key)
            self.connection.post_request(
                f"/games/{self.game_id}/mods/{mod_id}/ratings", data={"rating": rating.value}
            )
        except modioException:
            return False

        return True

    async def _async_add_rating(self, rating: RatingType):
        try:
            mod_id = getattr(self, self.mod_key)
            await self.connection.async_post_request(
                f"/games/{self.game_id}/mods/{mod_id}/ratings", data={"rating": rating.value}
            )
        except modioException:
            return False

        return True

    def add_positive_rating(self):
        """Changes the mod rating to positive, the author of the rating will be the authenticated user.
        If the mod has already been positevely rated by the user it will return False. If the positive rating
        is successful it will return True.

        |coro|"""
        return self._add_rating(RatingType.good)

    async def async_add_positive_rating(self):
        return await self._async_add_rating(RatingType.good)

    def add_negative_rating(self):
        """Changes the mod rating to negative, the author of the rating will be the authenticated user.
        If the mod has already been negatively rated by the user it will return False. If the negative rating
        is successful it will return True.

        |coro|"""
        return self._add_rating(RatingType.bad)

    async def async_add_negative_rating(self):
        return await self._async_add_rating(RatingType.bad)

    def delete(self):
        """Removes a rating. Returns true if the rating was succefully removed.

        |coro|
        """
        return self._add_rating(RatingType.neutral)

    async def async_delete(self):
        return await self._async_add_rating(RatingType.neutral)


class OwnerMixin:
    """Mixin containing get owner methods."""

    def get_owner(self):
        """Get the original submitter of the resource.

        |coro|

        Returns
        -------
        User
            The original submitter
        """
        user = self.connection.post_request(
            "/general/ownership", data={"resource_type": self.resource_type, "resource_id": self.id}
        )
        return entities.User(connection=self.connection, **user)

    async def async_get_owner(self):
        user = await self.connection.async_post_request(
            "/general/ownership", data={"resource_type": self.resource_type, "resource_id": self.id}
        )
        return entities.User(connection=self.connection, **user)
