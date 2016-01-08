``mkjsubs.py`` generates the submission scripts in ``./jsubs``

``jsub.sh`` submits them and moves them to ``./jsubs-subbed``

``generateLists.sh`` is used to generate file lists

In all cases ``pwd`` should be at the same level as this ``scripts`` directory.

---

All other scripts are for cleanup/diagnostics/testing.

---

TODO: Remove dependence on ``generateLists.sh`` by ``mkjsubs.py``

TODO: Let ``mkjsub.py`` regenerate raw tape list every time instead of doing it manually.

TODO: Remove hardcoding of top level dir for next run (e.g. ``/u/group/hps/production/data/EngRun2015`` and ``/work/hallb/hps/data/engrun2015``)
