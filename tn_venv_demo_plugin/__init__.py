"""A trivial tn-venv plugin."""

from __future__ import annotations

from tn_venv.plugins import HookName, Plugin


class DemoPlugin(Plugin):
    """Logs a line at session start and captures the env dir at session end."""

    # Stable identifier; required by Plugin. The loader emits this as
    # the "name" column in ``tn-venv --list-plugins`` output.
    name = "demo_plugin"

    def register(self, hooks) -> None:
        # Hooks.add() accepts either a callable directly or a
        # decorator; both forms are demonstrated here.
        hooks.add(
            HookName.SESSION_START,
            self._on_session_start,
            priority=100,           # DEFAULT_PRIORITY is 100
            plugin_name=self.name,
        )

        @hooks.add(HookName.SESSION_END, plugin_name=self.name)
        def _on_session_end(ctx):
            # SESSION_END is the only lifecycle hook where ctx.result
            # is guaranteed to be populated.
            env_dir = ctx.result.env_dir if ctx.result else None
            ctx.reporter.info(
                f"[demo_plugin] session ended; env_dir = {env_dir}"
            )

    def _on_session_start(self, ctx) -> None:
        # SESSION_START fires after option resolution and interpreter
        # discovery, but before the destination lock is acquired.
        ctx.reporter.info("hello from demo_plugin")