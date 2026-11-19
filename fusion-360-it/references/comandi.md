# Comandi di Fusion: nome, identificativo, API, Personal, provato

Elenco dei 1 665 comandi dell'interfaccia di Fusion (in italiano, nov. 2026), abbinati all'API dove esiste. **Non leggerlo intero**: cerca il nome del comando (italiano) o l'identificativo (`Ctrl+F`/Grep). «API —» = nessun oggetto dell'API abbinato: il comando si usa dall'interfaccia. «Provato» = l'oggetto API compare nel codice delle ricette provate (non garantisce ogni variante).

## Indice

- Progetto (Design) / Scheda SOLIDO (`SolidTab`): 163
- Progetto (Design) / Scheda SUPERFICIE (`SurfaceTab`): 20
- Progetto (Design) / Scheda Mesh (`ParaMeshOuterTab`): 29
- Progetto (Design) / Scheda FORMA (`FormTab`): 48
- Progetto (Design) / Scheda LAMIERA (`SheetMetalTab`): 17
- Progetto (Design) / Scheda PLASTICA (`PlasticTab`): 7
- Progetto (Design) / Scheda ASSIEME (`AssemblyTab`): 1
- Progetto (Design) / Scheda GESTISCI (`ManageTab`): 9
- Progetto (Design) / Scheda UTILITÀ (`ToolsTab`): 11
- Progetto (Design) / Scheda AUTOMAZIONE (`AutomationTab`): 2
- Progetto (Design) / Scheda PCB (`PCBTab`): 7
- Progetto (Design) / Scheda Pacchetto (`Package3DTab`): 48
- Progetto (Design) / Scheda SOLIDO (`BasefeatureSolidTab`): 1
- Progetto (Design) / Scheda SCHIZZO (`SketchTab`): 67
- Progetto (Design) / Scheda POSIZIONE (`EditSnapshotTab`): 2
- Progetto (Design) / Scheda Modifica diretta della mesh (`ParaMeshBaseFeatureTab`): 1
- Progetto (Design) / Scheda menu (File, barre fisse, tasto destro, radiale) (`Menu`): 446
- Produzione (Manufacture, CNC) / Scheda Fresatura (`MillingTab`): 88
- Produzione (Manufacture, CNC) / Scheda Tornitura (`TurningTab`): 17
- Produzione (Manufacture, CNC) / Scheda Additivo (`AdditiveTab`): 43
- Produzione (Manufacture, CNC) / Scheda Risultati (`AdditiveResultsTab`): 8
- Produzione (Manufacture, CNC) / Scheda Ispezione (`ProbingTab`): 14
- Produzione (Manufacture, CNC) / Scheda Fabbricazione (`FabricationTab`): 7
- Produzione (Manufacture, CNC) / Scheda Utilità (`UtilitiesTab`): 3
- Produzione (Manufacture, CNC) / Scheda Allineamento parte (`PartAlignmentTab`): 8
- Produzione (Manufacture, CNC) / Scheda Allineamento parte in tempo reale (`LiveAlignmentTab`): 3
- Produzione (Manufacture, CNC) / Scheda Simulazione (`SimulationTab`): 12
- Produzione (Manufacture, CNC) / Scheda menu (File, barre fisse, tasto destro, radiale) (`Menu`): 207
- Disegno (Drawing) / Scheda DISEGNO (`FusionDocTab`): 103
- Disegno (Drawing) / Scheda COMPONENTI ELETTRONICI (`ElectronicsTab`): 5
- Disegno (Drawing) / Scheda GESTISCI (`ManageTab`): 1
- Disegno (Drawing) / Scheda CARTIGLIO (`TitleBlockTab`): 8
- Disegno (Drawing) / Scheda menu (File, barre fisse, tasto destro, radiale) (`Menu`): 79
- Rendering / Scheda RENDERING (`RenderTab`): 9
- Rendering / Scheda menu (File, barre fisse, tasto destro, radiale) (`Menu`): 4
- Animazione / Scheda ANIMAZIONE (`Animation`): 10
- Animazione / Scheda menu (File, barre fisse, tasto destro, radiale) (`Menu`): 29
- Comuni (menu File e barre fisse) / Scheda menu (File, barre fisse, tasto destro, radiale) (`Menu`): 128

## Progetto (Design) / Scheda SOLIDO (`SolidTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Crea schizzo | `SketchCreate` | `Sketches` | sì (presente) | sì |
| Crea forma | `TSplineBaseFeatureCreationCommand` | `FormFeatures.add` | sì (presente) | sì |
| Deriva | `PushDeriveCommand` | `DeriveFeatures` | sì (presente) | sì |
| Modellazione automatica | `AutomatedModelingCommand` | — | modellazione automatica / generativa: no | — |
| Estrusione | `Extrude` | `ExtrudeFeatures` | sì (presente) | sì |
| Rivoluzione | `Revolve` | `RevolveFeatures` | sì (presente) | sì |
| Sweep | `Sweep` | `SweepFeatures` | sì (presente) | sì |
| Loft | `SolidLoft` | `LoftFeatures` | sì (presente) | sì |
| Nervatura | `FusionRibCommand` | `RibFeatures` | sì (presente) | sì |
| Maglia | `FusionWebCommand` | `WebFeatures` | sì (presente) | no |
| Sbalzo | `EmbossCmd` | `EmbossFeatures` | sì (presente) | sì |
| Foratura | `FusionHoleCommand` | `HoleFeatures` | sì (presente) | sì |
| Filettatura | `FusionThreadCommand` | `ThreadFeatures` | sì (presente) | sì |
| Parallelepipedo | `PrimitiveBox` | `BoxFeatures` | sì (presente) | no |
| Cilindro | `PrimitiveCylinder` | `CylinderFeatures` | sì (presente) | no |
| Sfera | `PrimitiveSphere` | `SphereFeatures` | sì (presente) | no |
| Toroide | `PrimitiveTorus` | `TorusFeatures` | sì (presente) | no |
| Elicoide | `PrimitiveCoil` | `CoilFeatures` | sì (presente) | sì |
| Tubo | `PrimitivePipe` | `PipeFeatures` | sì (presente) | sì |
| Solido di delimitazione | `StockModelCommand` | — | sì (presente) | — |
| Serie rettangolare | `PatternRectangular` | `RectangularPatternFeatures` | sì (presente) | sì |
| Serie circolare | `PatternCircular` | `CircularPatternFeatures` | sì (presente) | sì |
| Serie su traiettoria | `PatternOnPath` | `PathPatternFeatures` | sì (presente) | sì |
| Serie geometrica | `FusionPatternGeometricCommand` | — | sì (presente) | — |
| Specchio | `MirrorCommand` | `MirrorFeatures` | sì (presente) | sì |
| Ispessisci | `FusionSurfaceThickenCommand` | `ThickenFeatures` | sì (presente) | sì |
| Riempimento contorno | `SurfaceSculpt` | `BoundaryFillFeatures` | sì (presente) | no |
| Trova lavorazioni | `FusionFindFeaturesCommand` | — | sì (presente) | — |
| Volume fluido | `EnclosureCommand` | — | sì (presente) | — |
| Crea lavorazione di base | `BaseFeatureCreationCommand` | `BaseFeatures` | sì (presente) | sì |
| Crea PCB collegato | `PCBExternalComponentCreationCmd` | — | sì (presente) | — |
| Deriva PCB | `PCBDeriveCmd` | — | sì (presente) | — |
| Crea PCB non collegato | `PCBCreateCmd` | — | sì (presente) | — |
| Origine del giunto | `JointOrigin` | `JointOrigins` | sì (presente) | sì |
| Genera timeline | `TimelineBuilderCommand` | `Timeline` | sì (presente) | sì |
| Premere e trascinare | `FusionPressPullCommand` | `ExtrudeFeatures` | sì (presente) | sì |
| Modifica faccia | `EditFaceCommand` | — | sì (presente) | — |
| Raccordo | `FusionFilletEdgesCommand` | `FilletFeatures` | sì (presente) | sì |
| Smusso | `FusionChamferCommand` | `ChamferFeatures` | sì (presente) | sì |
| Svuotamento | `FusionShellBodyCommand` | `ShellFeatures` | sì (presente) | sì |
| Sformo | `FusionDraftCommand` | `DraftFeatures` | sì (presente) | sì |
| Scala | `ModifyScale` | `ScaleFeatures` | sì (presente) | sì |
| Combina | `FusionCombineCommand` | `CombineFeatures` | sì (presente) | sì |
| Offset faccia | `FusionOffsetFacesCommand` | `OffsetFacesFeatures` | sì (presente) | sì |
| Sostituisci faccia | `FusionReplaceFaceCommand` | `ReplaceFaceFeatures` | sì (presente) | no |
| Divisione faccia | `FusionSplitFaceCommand` | `SplitFaceFeatures` | sì (presente) | sì |
| Divisione corpo | `FusionSplitBodyCommand` | `SplitBodyFeatures` | sì (presente) | sì |
| Divisione sagoma | `FusionPartingLineSplitCmd` | `SilhouetteSplitFeatures` | sì (presente) | no |
| Sposta/Copia | `FusionMoveCommand` | `MoveFeatures` | sì (presente) | sì |
| Allinea | `AlignCmd` | — | sì (presente) | — |
| Elimina | `FusionDeleteCommand` | `Design.deleteEntities` | sì (presente) | no |
| Rimuovi | `SoftDeleteCommand` | `RemoveFeatures` | sì (presente) | no |
| Disponi | `ArrangeCommand` | `ArrangeFeatures` | sì (presente) | no |
| Rimuovi lavorazioni | `FusionRemoveFeaturesCommand` | `RemoveFeatures` | sì (presente) | no |
| Rimuovi facce | `FusionRemoveFacesCommand` | `RemoveFeatures` | sì (presente) | no |
| Sostituisci con primitive | `ReplaceWithPrimitivesCommand` | — | sì (presente) | — |
| Reticolo volumetrico | `VolFieldCreateLatticeCommand` | `VolumetricModelFeatures 🧪` | sì (presente) | no |
| Texture volumetrica | `VolFieldTextureCommand` | `VolumetricModelFeatures 🧪` | sì (presente) | no |
| Materiale fisico | `PhysicalMaterialCommand` | `Materials` | sì (presente) | sì |
| Aspetto | `AppearanceCommand` | `Appearances` | sì (presente) | sì |
| Gestione dei materiali | `MaterialCommand` | `Materials` | sì (presente) | sì |
| Modifica parametri | `ChangeParameterCommand` | `UserParameters` | sì (presente) | sì |
| Calcola tutto | `FusionComputeAllCommand` | `Design` | sì (presente) | sì |
| Calcola irrisolti | `FusionComputeUnresolvedCommand` | `Design` | sì (presente) | sì |
| Converti | `TSpline2BRepCommand` | `FormFeature.updateBRep` | sì (presente) | no |
| Distinta componenti | `MaterializedBomHybridCmd` | — | distinta e rilasci (Manage): no | — |
| Inserisci componente | `FusionImportCommandFromToolbar` | `ImportManager` | sì (presente) | sì |
| Nuovo componente | `FusionCreateNewComponentCommand` | `Occurrences` | sì (presente) | sì |
| Duplica con giunti | `FusionDuplicateWithJointsCommand` | — | sì (presente) | — |
| Vincola componenti | `AssemblyMateCommand` | `AssemblyConstraints 🧪` | sì (presente) | no |
| Vincolo di allineamento | `AlignConstraintCmd` | `AssemblyConstraints 🧪` | sì (presente) | no |
| Vincolo dell'angolo | `AngleConstraintCmd` | `AssemblyConstraints 🧪` | sì (presente) | no |
| Vincolo centro | `MidplaneConstraintCmd` | `AssemblyConstraints 🧪` | sì (presente) | no |
| Vincolo tangente | `TangentConstraintCmd` | `AssemblyConstraints 🧪` | sì (presente) | no |
| Vincolo giunto | `JointConstraintCmd` | `AssemblyConstraints 🧪` | sì (presente) | no |
| Giunto | `JointAssembleCmdNew` | `Joints` | sì (presente) | sì |
| Giunto come costruito | `JointAsBuiltCmd` | `AsBuiltJoints` | sì (presente) | sì |
| Vincolo come costruito | `AsBuiltConstraintCmd` | `AsBuiltJoints` | sì (presente) | sì |
| Gruppo rigido | `RigidGroupCmd` | `RigidGroups` | sì (presente) | sì |
| Aziona giunti | `FusionMoveJointsCommand` | `Joint.jointMotion` | sì (presente) | sì |
| Collegamento movimento | `FusionMotionRelationshipCommand` | `MotionLinks` | sì (presente) | no |
| Studio del movimento | `FusionMotionStudyCommand` | — | sì (presente) | — |
| Abilita gruppi di contatti | `EnableContactSetsCmd` | `Design.isContactSetAnalysis` | sì (presente) | no |
| Abilita tutti i contatti | `EnableAllContactCmd` | `Design.isContactAnalysisEnabled` | sì (presente) | no |
| Disabilita contatto | `DisableAllContactCmd` | `Design.isContactAnalysisEnabled` | sì (presente) | no |
| Nuovo gruppo di contatti | `ContactSetCmd` | `ContactSets` | sì (presente) | no |
| Configura | `FusionStartDesignConfigModeCmd` | — | configurazioni: no | — |
| Visualizza tabella di configurazione | `FusionShowDesignConfigPanelCmd` | — | configurazioni: no | — |
| Crea regole di configurazione | `FusionConfigurationRulesCmd` | — | configurazioni: no | — |
| Sistema di coordinate utente (UCS) | `CoordinateSystemCommand` | — | sì (presente) | — |
| Piano di offset | `ConstructionPlaneOffsetFromPlaneCommand` | `ConstructionPlaneInput` | sì (presente) | no |
| Piano in corrispondenza dell'angolo | `ConstructionPlaneAtAngleCommand` | `ConstructionPlaneInput` | sì (presente) | no |
| Piano tangente | `ConstructionTangentPlaneCommand` | `ConstructionPlaneInput` | sì (presente) | no |
| Piano medio | `ConstructionMidPlaneCommand` | `ConstructionPlaneInput` | sì (presente) | no |
| Piano perpendicolare | `ConstructionPlanePerpendicularToPlaneCommand` | `ConstructionPlaneInput` | sì (presente) | no |
| Piano attraverso due spigoli | `ConstructionPlaneFromTwoEdgesCommand` | `ConstructionPlaneInput` | sì (presente) | no |
| Piano attraverso tre punti | `ConstructionPlaneFromThreePointsCommand` | `ConstructionPlaneInput` | sì (presente) | no |
| Piano lungo la traiettoria | `ConstructionPlaneAlongPathCommand` | `ConstructionPlaneInput` | sì (presente) | no |
| Asse attraverso cilindro/cono/toroide | `ConstructionAxisThroughCylinderCommand` | `ConstructionAxisInput` | sì (presente) | no |
| Asse perpendicolare alla faccia | `ConstructionAxisNormalToFaceCommand` | `ConstructionAxisInput` | sì (presente) | no |
| Asse tra due piani | `ConstructionAxisFromTwoPlanesCommand` | `ConstructionAxisInput` | sì (presente) | no |
| Asse attraverso due punti | `ConstructionAxisThroughTwoPointsCommand` | `ConstructionAxisInput` | sì (presente) | no |
| Asse attraverso spigolo | `ConstructionAxisThroughEdgeCommand` | `ConstructionAxisInput` | sì (presente) | no |
| Punto in corrispondenza di un vertice | `ConstructionPointFromPointCommand` | `ConstructionPointInput` | sì (presente) | no |
| Punto attraverso due spigoli | `ConstructionPointThroughTwoEdgesCommand` | `ConstructionPointInput` | sì (presente) | no |
| Punto attraverso tre piani | `ConstructionPointFromThreePlanesCommand` | `ConstructionPointInput` | sì (presente) | no |
| Punto al centro del cerchio/della sfera/del toroide | `ConstructionPointFromCircleOrSphereCommand` | `ConstructionPointInput` | sì (presente) | no |
| Punto in corrispondenza di uno spigolo e di un piano | `ConstructionPointAtEdgeAndPlaneCommand` | `ConstructionPointInput` | sì (presente) | no |
| Punto lungo la traiettoria | `ConstructionPointAlongPathCommand` | `ConstructionPointInput` | sì (presente) | no |
| Misura | `MeasureCommand` | `MeasureManager` | sì (presente) | sì |
| Analisi sezione | `FusionHalfSectionViewCommand` | `SectionAnalyses` | sì (presente) | sì |
| Interferenza | `InterferenceCheckCommand` | `InterferenceInput` | sì (presente) | no |
| Centro di massa | `FusionCenterOfMassCommand` | `PhysicalProperties.centerOfMass` | sì (presente) | sì |
| Analisi pettini di curvatura | `FusionCurvatureCombAnalysisCommand` | `CurvatureCombAnalyses` | sì (presente) | no |
| Analisi mappa curvatura | `FusionCurvatureMapAnalysisCommand` | `CurvatureMapAnalyses` | sì (presente) | no |
| Analisi sformo | `FusionDraftAnalysisCommand` | `DraftAnalyses` | sì (presente) | sì |
| Analisi mappa ambiente | `FusionEnvironmentMapAnalysisCommand` | `EnvironmentMapAnalyses` | sì (presente) | no |
| Analisi isocurva | `FusionIsoCurveAnalysisCommand` | `IsoCurveAnalyses` | sì (presente) | no |
| Analisi Zebra | `FusionZebraAnalysisCommand` | `ZebraAnalyses` | sì (presente) | no |
| Convalida | `FusionSurfaceValidateCommand` | — | sì (presente) | — |
| Analisi accessibilità | `FusionAccessibilityAnalysisCommand` | `AccessibilityAnalyses` | sì (presente) | sì |
| Analisi raggio minimo | `FusionMinimumRadiusAnalysisCommand` | `MinimumRadiusAnalyses` | sì (presente) | sì |
| Analisi connessione componente | `FusionComponentConnectionAnalysisCommand` | — | sì (presente) | — |
| Analisi della pila di elementi di fissaggio | `FusionFastenerStackAnalysisCommand` | — | sì (presente) | — |
| Navigatore | `GraphViewCmd` | — | sì (presente) | — |
| Analisi GDL | `FusionDOFAnalysisCommand` | — | sì (presente) | — |
| Modifica analisi connessione componente | `FusionEditComponentConnectionAnalysisCommand` | — | sì (presente) | — |
| Visualizza colori componenti | `FusionViewColorCyclingToggleCmd` | — | sì (presente) | — |
| Visualizza gruppi di facce mesh | `FacegroupsToggleCmd` | `MeshBodyDisplayOverrides.isSuppressFaceGroupColors` | sì (presente) | no |
| Statistiche assieme | `FusionAssemblyStatisticsCommand` | — | sì (presente) | — |
| Trova componenti simili | `SimilarPartsCommand` | — | sì (presente) | — |
| Cronologia | `ShowHistoryToolbarCmd` | — | sì (presente) | — |
| Riepilogo modifiche | `ShowChangeAwarenessToolbarCmd` | — | sì (presente) | — |
| Sustainability Insights | `GravityClimate_ManufacturingSustainabilityInsights_MainDialog` | — | sì (presente) | — |
| Decalcomania | `FusionAddEditDecalCommand` | `Decals` | sì (presente) | no |
| Area grafica | `FusionAddCanvasCommand` | `Canvases` | sì (presente) | sì |
| Inserisci T-spline | `TSplineImportCommand` | `TSplineBodies.addByTSMFile` | sì (presente) | no |
| Inserisci SVG | `SketchImportSVG` | `Sketch.importSVG` | sì (presente) | sì |
| Inserisci file DXF | `ImportDxfFileCommand` | `ImportManager` | sì (presente) | sì |
| Inserisci mesh | `ParaMeshInsertAlignCommand` | `MeshBodies` | sì (presente) | sì |
| Inserisci elemento di fissaggio | `FusionFastenersCommand` | — | sì (presente) | — |
| Inserisci derivazione | `PullDeriveCommand` | `DeriveFeatures` | sì (presente) | sì |
| Inserisci componente McMaster-Carr | `InsertMcMasterCarrComponentCommand` | — | sì (presente) | — |
| Inserisci una parte produttore | `cadenasparts4cad` | — | sì (presente) | — |
| Inserire i componenti fornitore di TraceParts | `traceparts_insert` | — | sì (presente) | — |
| Aggiungi ad assieme | `NewAssemblyFromPartCommand` | `Occurrences` | sì (presente) | sì |
| Seleziona | `SelectCommand` | `Selections` | sì (presente) | no |
| Selezione con riquadro | `selectWindow` | `Selections` | sì (presente) | no |
| Selezione a forma libera | `selectFreeForm` | `Selections` | sì (presente) | no |
| Selezione a pennello | `selectPaint` | `Selections` | sì (presente) | no |
| Seleziona per nome | `SelectByNameCommand` | `Selections` | sì (presente) | no |
| Seleziona in base a contorno | `SelectByBoundaryCommand` | `Selections` | sì (presente) | no |
| Seleziona per dimensione | `FusionSelectBodiesBySizeCommand` | `Selections` | sì (presente) | no |
| Inverti selezione | `SelectByInvertCommand` | `Selections` | sì (presente) | no |
| Origine e contorno | `FusionSelectSeedAndBoundaryFacesCommand` | `Selections` | sì (presente) | no |
| Trascinamento componenti | `FusionDragCompControlsCmd` | — | sì (presente) | — |
| Priorità selezione corpo | `SelectBodyPriorityCommand` | `Selections` | sì (presente) | no |
| Priorità selezione facce | `SelectFacePriorityCommand` | `Selections` | sì (presente) | no |
| Priorità selezione spigolo | `SelectEdgePriorityCommand` | `Selections` | sì (presente) | no |
| Priorità selezione componente | `SelectComponentPriorityCommand` | `Selections` | sì (presente) | no |
| Filtri di selezione | `SelectionFilterCommand` | `Selections` | sì (presente) | no |
| Acquisizione della posizione | `SnapshotCmd` | `Snapshots` | sì (presente) | no |
| Ripristina posizione | `AsBuiltPositionsCmd` | `Snapshots.revertPendingSnapshot` | sì (presente) | no |

## Progetto (Design) / Scheda SUPERFICIE (`SurfaceTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Estrusione | `SurfaceExtrude` | `ExtrudeFeatures` | sì (presente) | sì |
| Rivoluzione | `SurfaceRevolve` | `RevolveFeatures` | sì (presente) | sì |
| Sweep | `SurfaceSweep` | `SweepFeatures` | sì (presente) | sì |
| Loft | `SurfaceLoft` | `LoftFeatures` | sì (presente) | sì |
| Delimita | `FusionSurfacePatchCommand` | `PatchFeatures` | sì (presente) | sì |
| Rigata | `FusionSurfaceRuledCommand` | `RuledSurfaceFeatures` | sì (presente) | no |
| Offset | `FusionSurfaceOffsetCommand` | `OffsetFeatures` | sì (presente) | no |
| Parallelepipedo | `SurfPrimitiveBox` | — | sì (presente) | — |
| Cilindro | `SurfPrimitiveCylinder` | — | sì (presente) | — |
| Sfera | `SurfPrimitiveSphere` | — | sì (presente) | — |
| Toroide | `SurfPrimitiveTorus` | — | sì (presente) | — |
| Elicoide | `SurfPrimitiveCoil` | — | sì (presente) | — |
| Tubo | `SurfPrimitivePipe` | — | sì (presente) | — |
| Ritaglia | `FusionSurfaceTrimCommand` | `TrimFeatures` | sì (presente) | no |
| Annulla taglio | `FusionSurfaceUntrimCommand` | `UntrimFeatures` | sì (presente) | no |
| Estendi | `FusionExtendCommand` | `ExtendFeatures` | sì (presente) | sì |
| Unisci | `FusionSurfaceStitchCommand` | `StitchFeatures` | sì (presente) | sì |
| Separa | `FusionSurfaceUnStitchCommand` | `UnstitchFeatures` | sì (presente) | no |
| Unisci | `FusionSurfaceMergeCommand` | `MergeFacesFeatures` | sì (presente) | no |
| Inverti normale | `FusionSurfaceReverseNormalCommand` | `ReverseNormalFeatures` | sì (presente) | no |

## Progetto (Design) / Scheda Mesh (`ParaMeshOuterTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Tessellazione | `ParaMeshTessellateCommand` | `MeshBodies.addByTriangleMeshData` | sì (presente) | no |
| Crea schizzo sezione mesh | `ParaMeshPlanarSectionCommand` | — | sì (presente) | — |
| Crea lavorazione mesh di base | `ParaMeshEmptyBaseFeatureCommand` | `BaseFeatures` | sì (presente) | sì |
| Ripristina | `ParaMeshRepairCommand` | `MeshRepairFeatures 🧪` | sì (presente) | sì |
| Genera gruppi di facce | `ParaMeshCalculateFaceGroupsCommand` | `MeshGenerateFaceGroupsFeatures 🧪` | sì (presente) | sì |
| Combina gruppi facce | `ParaMeshMergeFaceGroupsCommand` | `MeshCombineFaceGroupsFeatures 🧪` | sì (presente) | sì |
| Crea gruppo facce | `ParaMeshCreateFaceGroupCommand` | — | sì (presente) | — |
| Modifica diretta | `ParaMeshBaseFeatureCreateCommand` | `BaseFeatures` | sì (presente) | sì |
| Rigenera mesh | `ParaMeshRemeshCommand` | `MeshRemeshFeatures 🧪` | sì (presente) | sì |
| Riduci | `ParaMeshReduceCommand` | `MeshReduceFeatures 🧪` | sì (presente) | sì |
| Taglio piano | `ParaMeshPlaneCutCommand` | — | sì (presente) | — |
| Shell | `ParaMeshHollowCommand` | `MeshShellFeatures 🧪` | sì (presente) | sì |
| Unisci | `ParaMeshCombineCommand` | `MeshCombineFeatures 🧪` | sì (presente) | sì |
| Uniforme | `ParaMeshSmoothCommand` | `MeshSmoothFeatures 🧪` | sì (presente) | sì |
| Boundary uniforme | `ParaMeshSmoothBoundaryCommand` | — | sì (presente) | — |
| Inverti normale | `ParaMeshReverseNormalsCommand` | `MeshReverseNormalFeatures 🧪` | sì (presente) | sì |
| Chiudi crepe | `ParaMeshCloseCracksCommand` | — | sì (presente) | — |
| Cancella e Riempi | `ParaMeshEraseAndFillCommand` | — | sì (presente) | — |
| Ponte | `ParaMeshBridgeCommand` | — | sì (presente) | — |
| Allineamento mesh | `ParaMeshAlignCommand` | — | sì (presente) | — |
| Attrarre a riferimento | `ParaMeshAttractToReferenceCommand` | — | sì (presente) | — |
| Estrusione texture | `ParaMeshTextureCommand` | — | sì (presente) | — |
| Separa | `ParaMeshExtractCommand` | `MeshSeparateFeatures 🧪` | sì (presente) | sì |
| Scala mesh | `ParaMeshScaleCommand` | — | sì (presente) | — |
| Rimuovi | `ParaMeshRemoveCommand` | `MeshRemoveFeatures 🧪` | sì (presente) | sì |
| Converti mesh | `ParaMeshConvertCommand` | `MeshConvertFeatures 🧪` | sì (presente) | sì |
| Converti in mesh quadrangolare | `ParaMeshToQuadMeshCommand` | — | sì (presente) | — |
| Tavolozza mesh | `ParaMeshShowSelectionPanelCmd` | — | sì (presente) | — |
| Stampa 3D | `ThreeDprintCmdDef` | `ExportManager` | sì (presente) | sì |

## Progetto (Design) / Scheda FORMA (`FormTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Parallelepipedo | `TSplinePrimitiveBoxCommand` | `TSplineBodies.createBoxInput` | sì (presente) | sì |
| Piano | `TSplinePrimitivePlaneCommand` | `TSplineBodies.createPlaneInput` | sì (presente) | no |
| Cilindro | `TSplinePrimitiveCylinderCommand` | `TSplineBodies.createCylinderInput` | sì (presente) | no |
| Sfera | `TSplinePrimitiveSphereCommand` | `TSplineBodies.createSphereInput` | sì (presente) | sì |
| Toroide | `TSplinePrimitiveTorusCommand` | `TSplineBodies.createTorusInput` | sì (presente) | no |
| Quadball | `TSplinePrimitiveQuadBallCommand` | `TSplineBodies.createQuadballInput` | sì (presente) | sì |
| Tubo | `TSplinePrimitivePipe` | — | sì (presente) | — |
| Faccia | `TSplineAppendFaceCommand` | — | sì (presente) | — |
| Estrusione | `TSplineExtrudeCommand` | — | sì (presente) | — |
| Rivoluzione | `TSplineRevolveCommand` | — | sì (presente) | — |
| Sweep | `TSplineSweepCommand` | — | sì (presente) | — |
| Loft | `TSplineLoft` | — | sì (presente) | — |
| Modifica forma | `TSplineEditCommand` | — | sì (presente) | — |
| Modifica in base a curva | `TSplineEditByCurveCmd` | — | sì (presente) | — |
| Inserisci spigolo | `TSplineInsertEdgeCommand` | `FormFeature.insertEdge` | sì (presente) | no |
| Suddividi | `TSplineSubsetCmd` | — | sì (presente) | — |
| Inserisci punto | `TSplineInsertPointCommand` | — | sì (presente) | — |
| Unisci bordo | `TSplineMergeEdgeCmd` | — | sì (presente) | — |
| Ponte | `TSplineBridgeSubDCmd` | — | sì (presente) | — |
| Riempi foro | `TSplineFillHoleCmd` | — | sì (presente) | — |
| Cancella e Riempi | `TSplineEraseAndFillCmd` | — | sì (presente) | — |
| Salda vertici | `TSplineWeldCommand` | — | sì (presente) | — |
| Annulla saldatura spigoli | `TSplineUnWeldCommand` | — | sì (presente) | — |
| Piega | `TSplineCreasedEdgeCommand` | — | sì (presente) | — |
| Rimuovi piega | `TSplineUnCreaseEdgeCmd` | — | sì (presente) | — |
| Smussa spigolo | `TSplineBevelEdgeCommand` | — | sì (presente) | — |
| Scorri spigolo | `TSplineSlideEdgeCommand` | — | sì (presente) | — |
| Uniforma | `TSplineSmoothCmd` | — | sì (presente) | — |
| Rendi cilindrico | `TSplineCylindrifyCmd` | — | sì (presente) | — |
| Trascina | `TSplinePullSubDCmd` | — | sì (presente) | — |
| Livella | `TSplineFlattenSubDCmd` | — | sì (presente) | — |
| Raddrizza | `TSplineStraightenCmd` | — | nesting: estensione a pagamento — da verificare | — |
| Accoppia | `TSplineMatchCmd` | — | sì (presente) | — |
| Interpolazione | `TSplineInterpolateSubDCmd` | — | sì (presente) | — |
| Ispessisci | `TSplineThickenCommand` | — | sì (presente) | — |
| Congela | `TSplineFreezeCmd` | `FormFeatures` | sì (presente) | sì |
| Scongela | `TSplineUnFreezeCmd` | `FormFeatures` | sì (presente) | sì |
| Specchio - Interno | `TSplineInternalMirrorSymmetryCmd` | — | sì (presente) | — |
| Circolare - Interno | `TSplineInternalCircularSymmetryCmd` | — | sì (presente) | — |
| Specchio - Duplicato | `TSplineReflectionMirrorSymmetryCmd` | — | sì (presente) | — |
| Circolare - Duplicato | `TSplineReflectionCircularSymmetryCmd` | — | sì (presente) | — |
| Cancella simmetria | `TSplineClearSymmetryCommand` | — | sì (presente) | — |
| Isola simmetria | `TSplineIsolateSymmetryCmd` | — | sì (presente) | — |
| Modalità di visualizzazione | `TSplineToggleTessModeCmd` | `TSplineBody.displayMode` | sì (presente) | no |
| Ripara corpo | `TSplineRepairBodyCmd` | — | sì (presente) | — |
| Rendi uniforme | `TSplineMakeUniformCmd` | — | sì (presente) | — |
| Migliora prestazioni | `TSplineCapSettingCommand` | — | sì (presente) | — |
| Termina forma | `TSplineBaseFeatureStop` | `FormFeature.finishEdit` | sì (presente) | sì |

## Progetto (Design) / Scheda LAMIERA (`SheetMetalTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Flangia (Base/Spigolo/Contornatura) | `FusionSheetMetalFlangeCommand` | `FlangeFeatures` | sì (presente) | sì |
| Bordo | `FusionSheetMetalHemFlangeCommand` | `HemFeatures` | sì (presente) | no |
| Tramoggia | `FusionSheetMetalLoftCommand` | `LoftedFlangeFeatures 🧪` | sì (presente) | no |
| Piega | `SheetMetalFoldCmd` | `FoldFeatures 🧪` | sì (presente) | no |
| Converti in lamiera | `ConvertToSheetMetalCmd` | `BRepBody.convertToSheetMetal` | sì (presente) | sì |
| Converti in lamiera | `DMConvertToSheetMetalCmd` | `BRepBody.convertToSheetMetal` | sì (presente) | sì |
| Crea modello piatto | `FusionSheetMetalFlatPatternCmd` | `FlatPattern` | sì (presente) | no |
| Sviluppa | `FusionSheetmetalUnfoldCommand` | `UnfoldFeatures` | sì (presente) | sì |
| Regole lamiera | `FusionSheetMetalRulesCommand` | `SheetMetalRules` | sì (presente) | sì |
| Libreria di regole lamiera | `FusionSheetMetalRulesLibraryCommand` | `SheetMetalRules` | sì (presente) | sì |
| Chiusura angolo | `FusionSheetMetalCornerCommand` | `CornerClosureFeatures 🧪` | sì (presente) | no |
| Unisci per piega | `FusionJoinByBendCommand` | `JoinByBendFeatures 🧪` | sì (presente) | no |
| Separazione | `FusionSheetMetalRipCommand` | `RipFeatures` | sì (presente) | no |
| Riduzione | `FusionSheetMetalJogCommand` | — | sì (presente) | — |
| Raccordo lamiera | `FusionSheetMetalFilletCommand` | `FilletFeatures` | sì (presente) | sì |
| Smusso lamiera | `FusionSheetMetalChamferCommand` | `ChamferFeatures` | sì (presente) | sì |
| Ripiega | `FusionSheetmetalRefoldCommand` | `RefoldFeatures` | sì (presente) | sì |

## Progetto (Design) / Scheda PLASTICA (`PlasticTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Assegna regola plastica | `FusionAssignPlasticRuleCommand` | — | sì (presente) | — |
| Gestisci regole plastica | `FusionManagePlasticRuleCommand` | `PlasticRules.addByCopy` | sì (presente) | sì |
| Borchia | `FusionBossCommand` | `BossFeatures` | sì (presente) | no |
| Accoppiamento a scatto | `FusionSnapFitCommand` | — | sì (presente) | — |
| Bordo a incastro | `FusionLipCommand` | — | sì (presente) | — |
| Appoggio | `FusionRestCommand` | — | sì (presente) | — |
| Consigli di progettazione | `DesignAdviceCmd` | — | sì (presente) | — |

## Progetto (Design) / Scheda ASSIEME (`AssemblyTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Distinta componenti | `MaterializedBomCmd` | — | distinta e rilasci (Manage): no | — |

## Progetto (Design) / Scheda GESTISCI (`ManageTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Assegna numero elemento | `PIMAssignItemNumberCmd` | — | distinta e rilasci (Manage): no | — |
| Rilascio rapido | `PIMQuickReleaseCmd` | — | distinta e rilasci (Manage): no | — |
| Rilascia con ordine di modifica | `PIMECOReleaseCmd` | — | distinta e rilasci (Manage): no | — |
| Plancia di comando | `PIMGoToDashboardCmd` | — | sì (presente) | — |
| Dettagli | `PIMGoToItemDetailsCmd` | — | sì (presente) | — |
| Ordini di modifica | `PIMGoToChangeOrderCmd` | — | distinta e rilasci (Manage): no | — |
| Nuova attività | `TaskManagementCreateTaskCmd` | — | sì (presente) | — |
| Attività correlate | `TaskManagementRelatedTasksCmd` | — | sì (presente) | — |
| Apri sul sito | `TaskManagementOpenTasksCmd` | — | sì (presente) | — |

## Progetto (Design) / Scheda UTILITÀ (`ToolsTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Utensili di modellazione | `ModelingToggleCmdDef` | — | sì (presente) | — |
| Preparazione nest | `MSFNestAuthoringCmd` | — | nesting: estensione a pagamento — da verificare | — |
| Script e moduli aggiuntivi... | `ScriptsManagerCommand` | `Application` | sì (presente) | sì |
| Marketplace Design & Make | `ExchangeAppStoreCommand` | — | sì (presente) | — |
| API di Fusion | `APIHelpCommand` | `Application` | sì (presente) | sì |
| Gestisci libreria di filettature | `FusionManageThreadsLibraryCommand` | — | sì (presente) | — |
| Nota foro/filettatura | `HoleThreadNoteCommand` | `PMIHoleThreadNotes.add 🧪` | sì (presente) | sì |
| Nota | `LeaderLineNoteCommand` | `PMILeaderLineNotes.add 🧪` | sì (presente) | sì |
| Dimensioni e quote | `DimensionNoteCommand` | — | sì (presente) | — |
| Tolleranza geometrica | `GeometricToleranceNoteCommand` | — | sì (presente) | — |
| Nota generale | `GeneralNoteCommand` | — | sì (presente) | — |

## Progetto (Design) / Scheda AUTOMAZIONE (`AutomationTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| System Modeler | `FusionGraphExecutorAddinPaletteCmd` | — | sì (presente) | — |
| System Modeler Documentation | `SystemModelerAutomationDocsCmd` | — | sì (presente) | — |

## Progetto (Design) / Scheda PCB (`PCBTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Profilo PCB | `PCBDefineBoardCmd` | — | elettronica: skill a parte | — |
| Copia profilo EAGLE | `PCBImprintCmd` | — | elettronica: skill a parte | — |
| Modifica profilo EAGLE | `PCBBoardSketchEditCmd` | — | elettronica: skill a parte | — |
| Sposta componenti PCB | `PCBMoveComponentsCmd` | — | elettronica: skill a parte | — |
| Inverti componente | `PCBFlipComponentCmd` | — | elettronica: skill a parte | — |
| Stato PCB | `PCBStatusCmd` | — | elettronica: skill a parte | — |
| Termina PCB | `PCBStop` | — | elettronica: skill a parte | — |

## Progetto (Design) / Scheda Pacchetto (`Package3DTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Generatore pacchetti | `PackageGenerator` | — | elettronica: skill a parte | — |
| Generatore assiale | `cmd_id_Axial` | — | elettronica: skill a parte | — |
| Generatore BGA | `cmd_id_BGA` | — | elettronica: skill a parte | — |
| Generatore chip | `cmd_id_Chip` | — | elettronica: skill a parte | — |
| Generatore SOIC | `cmd_id_Soic` | — | elettronica: skill a parte | — |
| Generatore DFN-2 | `cmd_id_DFN2` | — | elettronica: skill a parte | — |
| Generatore DFN-3 | `cmd_id_DFN3` | — | elettronica: skill a parte | — |
| Generatore DFN-4 | `cmd_id_DFN4` | — | elettronica: skill a parte | — |
| Generatore connettore (maschio) con angolo a destra | `cmd_id_header_right_angle` | — | elettronica: skill a parte | — |
| Generatore connettore (femmina) con angolo a destra | `cmd_id_header_right_angle_socket` | — | elettronica: skill a parte | — |
| Generatore connettore (maschio) dritto | `cmd_id_header_straight` | — | elettronica: skill a parte | — |
| Generatore connettore (femmina) dritto | `cmd_id_header_straight_socket` | — | elettronica: skill a parte | — |
| Generatore SON | `cmd_id_Son` | — | elettronica: skill a parte | — |
| Generatore LED chip | `cmd_id_Chip_led` | — | elettronica: skill a parte | — |
| Generatore QFP | `cmd_id_Qfp` | — | elettronica: skill a parte | — |
| Generatore QFN | `cmd_id_Qfn` | — | elettronica: skill a parte | — |
| Serie di chip, generatore 2 lati convesso | `cmd_id_chiparray_2side_convex` | — | elettronica: skill a parte | — |
| Serie di chip, generatore 2 lati piatto/concavo | `cmd_id_chiparray_2side_flat_concave` | — | elettronica: skill a parte | — |
| Serie di chip, generatore 4 lati piatto/concavo | `cmd_id_chiparray_4side_flat` | — | elettronica: skill a parte | — |
| Generatore SOT143 | `cmd_id_sot143` | — | elettronica: skill a parte | — |
| Generatore SOT223 | `cmd_id_sot223` | — | elettronica: skill a parte | — |
| Generatore SOT23 | `cmd_id_sot23` | — | elettronica: skill a parte | — |
| Generatore SOTFL | `cmd_id_sotfl` | — | elettronica: skill a parte | — |
| Generatore PLCC | `cmd_id_Plcc` | — | elettronica: skill a parte | — |
| Generatore oscillatore a J | `cmd_id_Oscillator_j` | — | elettronica: skill a parte | — |
| Generatore oscillatore a l | `cmd_id_Oscillator_l` | — | elettronica: skill a parte | — |
| Generatore SOJ | `cmd_id_Soj` | — | elettronica: skill a parte | — |
| Generatore cristallo | `cmd_id_crystal` | — | elettronica: skill a parte | — |
| Generatore cristallo (HC49) | `cmd_id_crystal_hc49` | — | elettronica: skill a parte | — |
| Generatore DIP | `cmd_id_dip` | — | elettronica: skill a parte | — |
| Generatore calotta elettronica | `cmd_id_ecap` | — | elettronica: skill a parte | — |
| Generatore MELF | `cmd_id_Melf` | — | elettronica: skill a parte | — |
| Generatore stampato | `cmd_id_Molded` | — | elettronica: skill a parte | — |
| Generatore distanziale femmina | `cmd_id_female_standoff` | — | elettronica: skill a parte | — |
| Generatore distanziale maschio-femmina | `cmd_id_male_female_standoff` | — | elettronica: skill a parte | — |
| Generatore SOD | `cmd_id_Sod` | — | elettronica: skill a parte | — |
| Generatore blocco a innesto | `cmd_id_Snaplock` | — | elettronica: skill a parte | — |
| Generatore radiale | `cmd_id_Radial` | — | elettronica: skill a parte | — |
| Generatore LED circolare radiale | `cmd_id_Radial_Round_Led` | — | elettronica: skill a parte | — |
| Generatore concavo angolare | `cmd_id_Cornerconcave` | — | elettronica: skill a parte | — |
| Generatore SODFL | `cmd_id_Sodfl` | — | elettronica: skill a parte | — |
| Generatore A/DPAK | `cmd_id_TODPAK` | — | elettronica: skill a parte | — |
| Generatore diritto (femmina) connettore con montaggio su superficie | `cmd_id_surafce_mount_header_female` | — | elettronica: skill a parte | — |
| Generatore connettore (maschio) dritto con montaggio su superficie | `cmd_id_surface_mount_pin_header_male` | — | elettronica: skill a parte | — |
| Generatore connettore (maschio) con angolo retto e montaggio su superficie | `cmd_id_surface_mount_pin_header_male_right_angle` | — | elettronica: skill a parte | — |
| Generatore connettore DIP | `cmd_id_dip_socket` | — | elettronica: skill a parte | — |
| Generatore rettangolo con immersione radiale | `cmd_id_Radial_Dipped_Rectangle` | `SketchLines` | elettronica: skill a parte | sì |
| Fine | `Package3DStop` | — | elettronica: skill a parte | — |

## Progetto (Design) / Scheda SOLIDO (`BasefeatureSolidTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Termina lavorazione di base | `BaseFeatureStop` | `BaseFeatures` | sì (presente) | sì |

## Progetto (Design) / Scheda SCHIZZO (`SketchTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Linea | `DrawPolyline` | `SketchLines` | sì (presente) | sì |
| Linea punto medio | `SketchMidpointLine` | `SketchLines` | sì (presente) | sì |
| Rettangolo mediante 2 punti | `ShapeRectangleTwoPoint` | `SketchLines` | sì (presente) | sì |
| Rettangolo mediante 3 punti | `ShapeRectangleThreePoint` | `SketchLines` | sì (presente) | sì |
| Rettangolo mediante centro | `ShapeRectangleCenter` | `SketchLines` | sì (presente) | sì |
| Cerchio con centro-diametro | `CircleCenterRadius` | `SketchCircles` | sì (presente) | sì |
| Cerchio mediante 2 punti | `CircleTwoPoint` | `SketchCircles` | sì (presente) | sì |
| Cerchio mediante 3 punti | `CircleThreePoint` | `SketchCircles` | sì (presente) | sì |
| Cerchio a 2 tangenti | `CircleTanTanRadius` | `SketchCircles` | sì (presente) | sì |
| Cerchio mediante 3 tangenti | `CircleThreeTangent` | `SketchCircles` | sì (presente) | sì |
| Arco a 3 punti | `ArcThreePoint` | `SketchArcs` | sì (presente) | sì |
| Arco mediante centro e punto | `ArcCenterTwoPoint` | `SketchArcs` | sì (presente) | sì |
| Arco tangente | `ArcTangent` | `SketchArcs` | sì (presente) | sì |
| Poligono circoscritto | `ShapePolygonCircumscribed` | `SketchLines` | sì (presente) | sì |
| Poligono inscritto | `ShapePolygonInscribed` | `SketchLines` | sì (presente) | sì |
| Poligono da spigolo | `ShapePolygonEdge` | `SketchLines` | sì (presente) | sì |
| Ellisse | `CircleElipse` | `SketchEllipses` | sì (presente) | sì |
| Asola da centro a centro | `ShapeSlotCenterToCenter` | `SketchLines` | sì (presente) | sì |
| Asola sull'intera lunghezza | `ShapeSlotOverall` | `SketchLines` | sì (presente) | sì |
| Asola tramite punto centrale | `ShapeSlotCenterPoint` | `SketchLines` | sì (presente) | sì |
| Asola dell'arco mediante tre punti | `ShapeArcSlotThreePoint` | `SketchArcs` | sì (presente) | sì |
| Asola dell'arco mediante centro e punto | `ShapeArcSlotCenterTwoPoint` | `SketchArcs` | sì (presente) | sì |
| Spline punto di adattamento | `DrawSpline` | `SketchFittedSplines` | sì (presente) | sì |
| Spline punto di controllo | `DrawCVMSpline3D` | `SketchControlPointSplines` | sì (presente) | no |
| Spline punto di controllo | `DrawCVMSpline5D` | `SketchControlPointSplines` | sì (presente) | no |
| Curva conica | `ConicCurveCmd` | `SketchConicCurves` | sì (presente) | no |
| Punto | `DrawPoint` | `SketchPoints` | sì (presente) | no |
| Testo | `MTextCmd` | `SketchTexts` | sì (presente) | sì |
| Adatta curve a sezione mesh | `FitCurvesToSectionCommand` | `Sketch` | sì (presente) | no |
| Specchio | `MirrorSketchCommand` | `Sketch.mirror` | sì (presente) | sì |
| Serie circolare | `CircularSketchPatternCommand` | — | sì (presente) | — |
| Serie rettangolare | `RectangularSketchPatternCommand` | — | sì (presente) | — |
| Proietta | `ProjectNewCmd` | `Sketch.project` | sì (presente) | sì |
| Intersezione | `IntersectCmd` | `Sketch.intersectWithSketchPlane` | sì (presente) | sì |
| Profilo di rotazione | `SpunProfileCmd` | `Sketch.createSpunProfile` | sì (presente) | no |
| Includi geometria 3D | `Include3DGeometry` | `Sketch.include` | sì (presente) | no |
| Proietta su superficie | `ProjectToSurface` | `Sketch.projectToSurface` | sì (presente) | no |
| Curva di intersezione | `IntersectionCurve` | — | sì (presente) | — |
| Curva isoparametrica | `SketchIsoparametricCurve` | — | sì (presente) | — |
| Quota dello schizzo | `SketchDimension` | `SketchDimensions` | sì (presente) | sì |
| Raccordo | `FilletSketchCmd` | `SketchArcs.addFillet` | sì (presente) | sì |
| Uguale Distanza Smusso | `ChamferSketchEqualDistance` | `ChamferFeatures` | sì (presente) | sì |
| Smusso angolo e distanza | `ChamferSketchDistanceAngle` | `ChamferFeatures` | sì (presente) | sì |
| Due Distanza Smusso | `ChamferSketchDistanceDistance` | `ChamferFeatures` | sì (presente) | sì |
| Curva di raccordo diffuso | `BlendG1CurveSketchCmd` | `SketchFittedSplines.addBlendCurve` | sì (presente) | no |
| Offset | `Offset` | `Sketch.offset` | sì (presente) | sì |
| Ritaglia | `TrimSketchCmd` | `SketchCurve.trim` | sì (presente) | no |
| Estendi | `ExtendSketchCmd` | `SketchCurve.extend` | sì (presente) | sì |
| Interrompi | `BreakSketchCmd` | `SketchCurve.breakCurve` | sì (presente) | no |
| Scala schizzo | `SketchScaleCmd` | `Sketch.scale` | sì (presente) | sì |
| AutoConstrain | `SketchAutoConstraintAndDimCmd` | — | AutoConstrain: no (provato) | — |
| AutoConstrain da riferimento | `SketchAutoConstraintAndDimFromDatumCmd` | — | AutoConstrain: no (provato) | — |
| Orizzontale/Verticale | `ConstraintHorizontalVertical` | `GeometricConstraints` | sì (presente) | sì |
| Coincidente | `ConstraintCoincident` | `GeometricConstraints` | sì (presente) | sì |
| Tangente | `ConstraintTangent` | `GeometricConstraints` | sì (presente) | sì |
| Uguale | `ConstraintEqual` | `GeometricConstraints` | sì (presente) | sì |
| Parallelo | `ConstraintParallel` | `GeometricConstraints` | sì (presente) | sì |
| Perpendicolare | `ConstraintPerpendicular` | `GeometricConstraints` | sì (presente) | sì |
| Fisso/mobile | `ConstraintFix` | `GeometricConstraints` | sì (presente) | sì |
| PuntoMedio | `ConstraintMidPoint` | `GeometricConstraints` | sì (presente) | sì |
| Concentrico | `ConstraintConcentric` | `GeometricConstraints` | sì (presente) | sì |
| Collineare | `ConstraintCollinear` | `GeometricConstraints` | sì (presente) | sì |
| Simmetria | `ConstraintSymmetry` | `GeometricConstraints` | sì (presente) | sì |
| Curvatura | `ConstraintSmooth` | `GeometricConstraints` | sì (presente) | sì |
| Poligono | `SketchPolygonConstraintCmd` | `SketchLines` | sì (presente) | sì |
| Termina schizzo | `SketchStop` | `Sketch` | sì (presente) | no |
| Termina con AutoConstrain | `SketchAutoConstrainAndFinish` | — | AutoConstrain: no (provato) | — |

## Progetto (Design) / Scheda POSIZIONE (`EditSnapshotTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Termina posizione | `SnapshotEditAccept` | `Snapshots` | sì (presente) | no |
| Annulla posizione | `SnapshotEditCancel` | `Snapshots` | sì (presente) | no |

## Progetto (Design) / Scheda Modifica diretta della mesh (`ParaMeshBaseFeatureTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Termina modifica diretta | `ParaMeshBaseFeatureStopCommand` | `BaseFeature.finishEdit` | sì (presente) | sì |

## Progetto (Design) / Scheda menu (File, barre fisse, tasto destro, radiale) (`Menu`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Ripeti... | `RepeatCommand` | — | sì (presente) | — |
| Ripeti | `RedoCommand` | — | sì (presente) | — |
| Annulla | `UndoCommand` | — | sì (presente) | — |
| Panoramica | `PanCommand` | `Viewport.camera` | sì (presente) | sì |
| Zoom | `ZoomCommand` | `Viewport.camera` | sì (presente) | sì |
| Orbita vincolata | `ConstrainedOrbitCommand` | `Viewport.camera` | sì (presente) | sì |
| Imposta centro dell'orbita | `SetOrbitCenterCommand` | `Viewport.camera` | sì (presente) | sì |
| Ripristina centro dell'orbita | `ResetOrbitCenterCommand` | `Viewport.camera` | sì (presente) | sì |
| Allinea componenti | `AlignComponentsCmd` | — | sì (presente) | — |
| Allinea | `AlignGeometryCmd` | — | sì (presente) | — |
| Aggiorna modello piatto | `UpdateFlatPatternCommand` | `FlatPattern` | sì (presente) | no |
| Modifica diretta | `BeginEditInPlaceCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Modifica riferimento assieme | `BeginEIPAsEditContextCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Sincronizza riferimento assieme | `ContextUpdateFromParentCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Termina Modifica diretta | `EndEditInPlaceCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Attiva | `FusionActivateLocalCompCmd` | `Occurrence.activate` | sì (presente) | sì |
| Attiva riferimento assieme | `EIPContextActivateCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Interrompi collegamento | `EIPContextBreakLinkCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Sincronizza riferimento assieme | `EIPContextUpdateCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Sincronizza tutti i riferimenti assieme | `EIPContextsUpdateCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Sincronizza tutti i riferimenti assieme | `ContextUpdateAllFromParentCmd` | — | Modifica sul posto (Edit in Place): no | — |
| Attiva | `FusionSheetMetalFlatPatternActivateCmd` | `FlatPattern` | sì (presente) | no |
| Aggiorna modello piatto | `UpdateFlatPatternFromMainDesignCommand` | `FlatPattern` | sì (presente) | no |
| Aggiorna tutti i modelli piatti | `UpdateAllFlatPatternsCommand` | `FlatPattern` | sì (presente) | no |
| Blocca | `FusionGroundComponentsCommand` | `Occurrence.isGrounded` | sì (presente) | sì |
| Sblocca | `FusionUnGroundComponentsCommand` | `Occurrence.isGrounded` | sì (presente) | sì |
| Fissa a principale | `GroundToParentCommand` | `Occurrence.isGroundToParent` | sì (presente) | no |
| Svincolato da principale | `UnGroundToParentCommand` | `Occurrence.isGroundToParent` | sì (presente) | no |
| Rendi rigido | `RigidSubAssemblyCommand` | — | sì (presente) | — |
| Rendi flessibile | `FlexibleSubAssemblyCommand` | — | sì (presente) | — |
| Modifica lavorazione  | `FusionDcMoveBodyEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcMoveCopyEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica della posizione iniziale  | `FusionDcEditInitialPositionCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica della posizione iniziale  | `FusionEditInitialPositionCommand` | `Occurrence.initialTransform` | sì (presente) | no |
| Modifica lavorazione  | `FusionDcAlignEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Sposta nel gruppo | `FusionMoveToSurfaceGroupCommand` | `MoveFeatures` | sì (presente) | sì |
| Sposta nel gruppo | `FusionMoveToWorkGeometryCustomGroupCommand` | `MoveFeatures` | sì (presente) | sì |
| Sposta nel gruppo | `FusionMoveToSketchCustomGroupCommand` | `MoveFeatures` | sì (presente) | sì |
| Cambia configurazione | `FusionComponentChangeConfigCommand` | — | configurazioni: no | — |
| Crea componenti dai corpi | `FusionCreateNewCompCmdFromBody` | `BRepBody.createComponent` | sì (presente) | sì |
| Nuovo componente | `FusionCreateNewCompCmdFromSel` | `Occurrences.addNewComponent` | sì (presente) | sì |
| Modifica lavorazione  | `FusionCreateComponentFromBodyEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Crea disegno | `FusionDrawingCreateFromComponentsCommand` | `DrawingManager.createDrawing 🧪` | sì (presente) | no |
| Nuovo gruppo | `FusionCreateSurfaceGroupCommand` | — | sì (presente) | — |
| Nuovo gruppo di schizzi | `FusionCreateSketchCustomGroupCommand` | — | sì (presente) | — |
| Nuovo gruppo | `FusionCreateWorkGeometryCustomGroupCommand` | — | sì (presente) | — |
| Crea gruppo di selezione | `CreateSelectionGroupCmd` | `Selections` | sì (presente) | no |
| Modifica schizzo | `SketchActivate` | `Sketches.itemByName` | sì (presente) | sì |
| Ridefinsci piano dello schizzo | `SketchRedefineCommand` | `Sketch.redefine` | sì (presente) | no |
| Seleziona piano dello schizzo | `SelectSketchPlaneCommand` | `Selections` | sì (presente) | no |
| Gestisci proiezioni perse | `SketchRelinkProjectionCmd` | — | sì (presente) | — |
| Modifica lavorazione  | `FusionDcEditCanvasCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Calibra | `FusionDcCalibrateCanvasCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `FusionDcEditDecalCommand` | `Decals` | sì (presente) | no |
| Modifica raccordo | `FusionFilletEditCommand` | `FilletFeatures` | sì (presente) | sì |
| Modifica smusso | `FusionChamferEditCommand` | `ChamferFeatures` | sì (presente) | sì |
| Modifica foro | `FusionHoleEditCommand` | `HoleFeatures` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcHoleEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| DcBoltConnEdit | `DcBoltConnEdit` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionLoftEditCommand` | `LoftFeatures` | sì (presente) | sì |
| Modifica lavorazione  | `FusionSurfaceLoftEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcRibEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica filettatura | `FusionThreadEditCommand` | `ThreadFeatures` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcThreadEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica serie circolare | `PatternCircularEdit` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica serie rettangolare | `PatternRectangularEdit` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica serie circolare | `FusionDcCircularPatternEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcComplexPatternEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica serie su traiettoria | `FusionDcPathPatternEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica serie rettangolare | `FusionDcRectangularPatternEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcMirrorPatternEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica serie su traiettoria | `PatternOnPathEdit` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcDraftEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `FusionDcEmbossEditCmd` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica tubo | `TSplinePipeEditCommand` | `FormFeatures` | sì (presente) | sì |
| Modifica corrispondenza | `TSplineMatchEditCmd` | `FormFeatures` | sì (presente) | sì |
| Modifica lavorazione  | `FusionSurfacePatchEditCommand` | `PatchFeatures` | sì (presente) | sì |
| Modifica lavorazione  | `FusionSurfaceStitchEditCommand` | `StitchFeatures` | sì (presente) | sì |
| Modifica lavorazione  | `FusionSurfaceUnStitchEditCommand` | `UnstitchFeatures` | sì (presente) | no |
| Modifica lavorazione  | `FusionDcSurfaceDeleteFaceEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcReverseNormalEdit` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcSurfaceOffsetEditCommand` | `OffsetFeatures` | sì (presente) | no |
| Modifica lavorazione  | `FusionDcSurfaceOffsetShellEditCommand` | `OffsetFeatures` | sì (presente) | no |
| Modifica lavorazione  | `FusionDcMidSurfaceEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcSurfaceShellEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcSurfaceTrimEditCommand` | `TrimFeatures` | sì (presente) | no |
| Modifica lavorazione  | `FusionDcSurfaceUntrimEditCommand` | `UntrimFeatures` | sì (presente) | no |
| Modifica lavorazione  | `FusionDcSurfaceExtendEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcSurfaceRuledEditCommand` | `RuledSurfaceFeatures` | sì (presente) | no |
| Modifica lavorazione  | `FusionDcWebEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcScaleEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `DcReplaceWithPrimitiveEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica Rimuovi facce | `FusionRemoveFacesEditCommand` | `RemoveFeatures` | sì (presente) | no |
| Modifica Rimuovi lavorazioni | `FusionRemoveFeaturesEditCommand` | `RemoveFeatures` | sì (presente) | no |
| Modifica lavorazione  | `DCFusionGapFillEditCmd` | `TimelineObject.rollTo` | sì (presente) | sì |
| Taglia schizzo | `SliceSketchCommand` | `Sketch.isModelSliced` | sì (presente) | no |
| Elimina suddivisioni schizzo | `UnsliceSketchCommand` | `Sketch.isModelSliced` | sì (presente) | no |
| Abilita controllo completamente vincolato | `EnableFullyConstrained` | `Sketch.isFullyConstrained` | sì (presente) | sì |
| Disabilita controllo completamente vincolato | `DisableFullyConstrained` | — | sì (presente) | — |
| Modifica serie circolare | `SketchPatternCircularEdit` | `Sketch` | sì (presente) | no |
| Modifica serie rettangolare | `SketchRectangularPatternEdit` | `RectangularPatternFeatures` | sì (presente) | sì |
| Interrompi collegamento | `SketchUnProjectCmd` | `Sketch` | sì (presente) | no |
| Modifica testo | `EditTextCmd` | `SketchText.text` | sì (presente) | sì |
| Modifica testo | `EditMTextCmd` | `SketchTexts` | sì (presente) | sì |
| Esplodi testo | `ExplodeTextCmd` | `SketchText.explode` | sì (presente) | no |
| Normale/Costruzione | `SketchConstructionCmd` | `SketchCurve.isConstruction` | sì (presente) | sì |
| Normale/Linea d'asse | `SketchCenterLineCmd` | `SketchLine.isCenterLine` | sì (presente) | sì |
| Testo su percorso | `TextOnPathCmd` | `AlongPathTextDefinition` | sì (presente) | no |
| Modifica curva isoparametrica | `Include3DIsoParamCurveCmdEdit` | `Sketch` | sì (presente) | no |
| Modifica lavorazione | `DcBossEdit` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `DcSnapFitEdit` | — | sì (presente) | — |
| Modifica lavorazione | `DcRestEdit` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `DcLipEdit` | `TimelineObject.rollTo` | sì (presente) | sì |
| Fisso/mobile | `SketchFixConstraintCmd` | `SketchCurve.isFixed` | sì (presente) | no |
| Elimina coincidenti | `DeleteCoincidentConstraintCmd` | — | sì (presente) | — |
| Spostare nel piano dello schizzo | `SketchConstrainOnPlaneCmd` | — | sì (presente) | — |
| Salva schizzo con nome | `SaveSketchAsDWG` | `Documents.add` | sì (presente) | sì |
| Apri/Chiudi curva di spline | `SplineCloseCurve` | `SketchFittedSplines` | sì (presente) | sì |
| Inserisci punto di adattamento spline | `SplineInsertPoint` | `SketchFittedSplines` | sì (presente) | sì |
| Inserisci punto di controllo spline | `InsertControlPoint` | — | sì (presente) | — |
| Visualizza riquadro di controllo | `InsertControlPolygon` | `SketchLines` | sì (presente) | sì |
| Attiva maniglia tangente | `AddTangentHandle` | `SketchFittedSpline.activateTangentHandle` | sì (presente) | no |
| Attiva maniglia di curvatura | `AddCurvatureHandle` | `SketchFittedSpline.activateCurvatureHandle` | sì (presente) | no |
| Disattiva maniglia di curvatura | `DeleteCurvatureCommand` | — | sì (presente) | — |
| Disattiva maniglia tangente | `DeleteTangentCommand` | — | sì (presente) | — |
| Attiva/disattiva la visualizzazione della curvatura | `FusionToggleSetupCurveCurvatureCombCommand` | `CurvatureCombAnalyses` | sì (presente) | no |
| Imposta visualizzazione curvatura | `FusionCurveCurvatureCombSetupCommand` | `CurvatureCombAnalyses` | sì (presente) | no |
| Modifica PMI | `EditHoleThreadNoteCommand` | `PMIHoleThreadNote 🧪` | sì (presente) | no |
| Modifica lavorazione | `DMEditHoleThreadNoteCommand` | — | sì (presente) | — |
| Converti in PMI Fusion | `ConvertImportedPMICommand` | `Documents.add` | sì (presente) | sì |
| Contrassegna come aggiornato | `ResetPMIStateCommand` | — | sì (presente) | — |
| Mostra PMI importato | `DisplayImportedPMICommand` | `Viewport.camera` | sì (presente) | sì |
| Modifica PMI | `EditLeaderLineNoteCommand` | `PMILeaderLineNote 🧪` | sì (presente) | no |
| Modifica annotazione | `DMEditLeaderLineNoteCommand` | — | sì (presente) | — |
| Modifica PMI | `EditDimensionNoteCommand` | — | sì (presente) | — |
| Modifica annotazione | `DMEditDimensionNoteCommand` | — | sì (presente) | — |
| Modifica PMI | `EditGeometricToleranceNoteCommand` | — | sì (presente) | — |
| Modifica annotazione | `DMEditGeometricToleranceNoteCommand` | — | sì (presente) | — |
| Modifica giunto  | `EditJointAssembleCmd` | `Joint.jointMotion` | sì (presente) | sì |
| Modifica giunto  | `DcEditJointAssembleCmd` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica giunto  | `DcEditJointAsBuiltCmd` | `AsBuiltJoints` | sì (presente) | sì |
| Modifica vincolo | `DcEditAssemblyMateCmd` | `Joints` | sì (presente) | sì |
| Modifica vincolo | `EditAssemblyMateCmd` | `Joints` | sì (presente) | sì |
| Modifica limiti movimento | `EditJointDOFLimitsCmd` | `JointLimits` | sì (presente) | no |
| Modifica limiti offset | `EditOffsetLimitsCmd` | — | sì (presente) | — |
| Modifica gruppo rigido  | `DcEditRigidGroupCmd` | `RigidGroups` | sì (presente) | sì |
| Modifica gruppo rigido  | `EditRigidGroupCmd` | `RigidGroups` | sì (presente) | sì |
| Blocca movimento | `LockJointDOFCmd` | `Joint.isLocked` | sì (presente) | no |
| Sblocca movimento | `UnlockJointDOFCmd` | `Joint.isLocked` | sì (presente) | no |
| Blocca movimento | `LockJointCmd` | `Joint.isLocked` | sì (presente) | no |
| Sblocca movimento | `UnlockJointCmd` | `Joint.isLocked` | sì (presente) | no |
| Sopprimi | `SuppressJointOccurrenceCmd` | `Joint.isSuppressed` | sì (presente) | sì |
| Scopri | `UnsuppressJointOccurrenceCmd` | `Joint.isSuppressed` | sì (presente) | sì |
| Sopprimi | `SuppressTransitionalRelationshipOccurrenceCmd` | — | sì (presente) | — |
| Scopri | `UnsuppressTransitionalRelationshipOccurrenceCmd` | — | sì (presente) | — |
| Sopprimi | `SuppressGeometricRelationshipOccurrenceCmd` | — | sì (presente) | — |
| Scopri | `UnsuppressGeometricRelationshipOccurrenceCmd` | — | sì (presente) | — |
| Sopprimi vincolo | `SuppressConstraintCmd` | `AssemblyConstraint.isSuppressed 🧪` | sì (presente) | sì |
| Scopri vincolo | `UnSuppressConstraintCmd` | `AssemblyConstraint.isSuppressed 🧪` | sì (presente) | sì |
| Sopprimi | `SuppressRigidGroupCmd` | `RigidGroups` | sì (presente) | sì |
| Scopri | `UnsuppressRigidGroupCmd` | `RigidGroups` | sì (presente) | sì |
| Anima giunto | `AnimateJointCmd` | — | sì (presente) | — |
| Anima relazioni giunto | `AnimateModelCmd` | — | sì (presente) | — |
| Crea versione | `CreateVersionCommandFromCtxMenu` | `Document.save` | sì (presente) | sì |
| Vai all'inizio | `RestoreJointCmd` | — | sì (presente) | — |
| Imposta come posizione iniziale | `RedefineJointHomeCmd` | — | sì (presente) | — |
| Modifica relazione tangente | `EditTransitionalRelationshipCmd` | — | sì (presente) | — |
| Modifica relazione tangente | `DcEditTransitionalRelationshipCmd` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica | `EditMotionRelationshipCmd` | `MotionLinks` | sì (presente) | no |
| Modifica lavorazione | `DcEditMotionRelationshipCmd` | `MotionLinks` | sì (presente) | no |
| Sopprimi | `SuppressMotionRelationshipCmd` | `MotionLinks` | sì (presente) | no |
| Scopri | `UnsuppressMotionRelationshipCmd` | `MotionLinks` | sì (presente) | no |
| Seleziona componenti | `SelectComponentsCmd` | `Selections` | sì (presente) | no |
| Seleziona componenti | `SelectTransRelComponentsCmd` | `Selections` | sì (presente) | no |
| Seleziona giunti collegati | `SelectMotionLinkJointsCmd` | `Selections` | sì (presente) | no |
| Modifica | `EditMotionStudyCmd` | `MotionLinks` | sì (presente) | no |
| Modifica origine giunto  | `EditJointOriginCmd` | `JointOrigins` | sì (presente) | sì |
| Modifica origine giunto  | `EditJointOriginR2Cmd` | `JointOrigins` | sì (presente) | sì |
| Modifica sistema di coordinate utente (UCS) | `EditCoordinateSystemR2Cmd` | `ConstructionPlanes` | sì (presente) | sì |
| Modifica | `EditContactSetCmd` | `ContactSets` | sì (presente) | no |
| Sopprimi | `SuppressContactSetCmd` | `ContactSets` | sì (presente) | no |
| Scopri | `UnsuppressContactSetCmd` | `ContactSets` | sì (presente) | no |
| Mostra/Nascondi corpi associati | `GhostedBodyToggleCommand` | — | sì (presente) | no |
| Modifica area grafica | `FusionEditCanvasCommand` | `Canvas.transform` | sì (presente) | sì |
| Calibra | `FusionCalibrateCanvasCommand` | `Canvas.transform` | sì (presente) | sì |
| Sostituire file di immagine dell'area grafica | `FusionReplaceCanvasImageCommand` | — | sì (presente) | — |
| Modifica decalcomania | `FusionEditDecalCommand` | `Decals` | sì (presente) | no |
| Sostituisci file di immagine | `FusionReplaceDecalImageCommand` | `Decals` | sì (presente) | no |
| Modifica | `FusionEditCurvatureCombAnalysisCommand` | `CurvatureCombAnalyses` | sì (presente) | no |
| Modifica | `FusionEditZebraAnalysisCommand` | `ZebraAnalyses` | sì (presente) | no |
| Modifica | `FusionEditEnvironmentMapAnalysisCommand` | `EnvironmentMapAnalyses` | sì (presente) | no |
| Modifica | `FusionEditDraftAnalysisCommand` | `DraftAnalyses` | sì (presente) | sì |
| Modifica | `FusionEditCurvatureMapAnalysisCommand` | `CurvatureMapAnalyses` | sì (presente) | no |
| Modifica | `FusionEditAccessibilityAnalysisCommand` | `AccessibilityAnalyses` | sì (presente) | sì |
| Modifica | `FusionEditHalfSectionViewCommand` | `SectionAnalyses` | sì (presente) | sì |
| Modifica | `FusionEditCenterOfMassCommand` | `PhysicalProperties` | sì (presente) | sì |
| Modifica | `FusionEditMinimumRadiusAnalysisCommand` | `MinimumRadiusAnalyses` | sì (presente) | sì |
| Modifica | `FusionEditIsoCurveAnalysisCommand` | `IsoCurveAnalyses` | sì (presente) | no |
| Modifica analisi pila elementi di fissaggio | `FusionEditFastenerStackAnalysisCommand` | — | sì (presente) | — |
| Nuova vista con nome | `AddNamedViewCommand` | `Viewport.camera` | sì (presente) | sì |
| Elimina | `RemoveNamedViewCommand` | `RemoveFeatures` | sì (presente) | no |
| Aggiorna vista con nome | `UpdateNamedViewCameraCommand` | `Viewport.camera` | sì (presente) | sì |
| Nuova luce | `AddNamedLightCommand` | `Lights 🧪` | sì (presente) | no |
| Modifica luce | `FusionEditNamedLightCommand` | `Lights 🧪` | sì (presente) | no |
| Assegna regola plastica | `FusionSwitchPlasticRuleCommand` | — | sì (presente) | — |
| Rimuovi regola plastica | `FusionRemovePlasticRuleCommand` | `RemoveFeatures` | sì (presente) | no |
| Dissolvi lavorazioni | `DissolveFeaturesCmdDef` | — | sì (presente) | — |
| Rendi indipendente | `FusionMakeIndependentCommand` | — | sì (presente) | — |
| Selezionare i giunti di riferimento | `SelectJointsByComponentCmd` | `Selections` | sì (presente) | no |
| Rimuovi sostituzione aspetto | `FusionRemoveOverrideCommand` | `RemoveFeatures` | sì (presente) | no |
| Proprietà | `FusionPropertiesCommand` | — | sì (presente) | — |
| Risolvi componente | `FusionResolveMissingXRefCmd` | — | sì (presente) | — |
| Sola lettura per utente corrente | `EnableReadOnlyCmd` | — | sì (presente) | — |
| Sola lettura per utente corrente | `DisableReadOnlyCmd` | — | sì (presente) | — |
| FlatMeshShadingCmd | `FlatMeshShadingCmd` | — | sì (presente) | — |
| SmoothMeshShadingCmd | `SmoothMeshShadingCmd` | — | sì (presente) | — |
| MeshTriangulateCommand | `MeshTriangulateCommand` | — | sì (presente) | — |
| FusionInsertComponentCommand | `FusionInsertComponentCommand` | `Occurrences.addByInsert` | sì (presente) | sì |
| Esporta... | `FusionExportComponentCommand` | `Documents.add` | sì (presente) | sì |
| Esporta serie piatta | `ExportFlatPatternCmd` | `FlatPattern` | sì (presente) | no |
| Salva copia con nome | `FusionSaveAsComponentCommand` | `Documents.add` | sì (presente) | sì |
| Salva progettazione configurata con nome | `FusionSaveAsConfiguredDesignCommand` | `Documents.add` | configurazioni: no | sì |
| Salva configurazione con nome | `FusionSaveAsConfigurationCommand` | `Documents.add` | configurazioni: no | sì |
| Salva configurazione con nome | `FusionCDSaveAsConfigurationCommand` | `Documents.add` | configurazioni: no | sì |
| Salva con nome e sostituisci | `FusionSaveAsAndReplaceComponentCommand` | `Documents.add` | sì (presente) | sì |
| Salva come più recente | `PLM360SaveAsLatestCommand` | `Documents.add` | sì (presente) | sì |
| Salva come mesh | `FusionSaveAsSTLCommand` | `Documents.add` | sì (presente) | sì |
| Salva in formato OBJ | `FusionSaveAsOBJCommand` | `Documents.add` | sì (presente) | sì |
| Salva riquadro di controllo come OBJ | `FusionSaveControlFrameAsOBJCommand` | `Documents.add` | sì (presente) | sì |
| Salva T-spline come IGA | `TSplineSaveAsIGACommand` | `FormFeatures` | sì (presente) | sì |
| Apri | `PLM360OpenAttachmentCommand` | `Documents.add` | sì (presente) | sì |
| Open Source | `OpenDeriveDocumentCommand` | `Documents.add` | sì (presente) | sì |
| Carica versione più recente | `PLM360RefreshDocumentCommand` | `Documents.add` | sì (presente) | sì |
| Carica versione più recente | `GetLatestCmd` | `DocumentReference.getLatestVersion` | sì (presente) | sì |
| Carica ultima versione del traguardo | `GetLatestMilestoneCmd` | — | sì (presente) | — |
| Aggiorna riferimenti esterni | `GetAllLatestCmd` | `DocumentReference.getLatestVersion` | sì (presente) | sì |
| Carica tutte le versioni più recenti | `UpdateAllLatestCmd` | `DocumentReference.getLatestVersion` | sì (presente) | sì |
| Mostra in posizione | `ShowInLocationCmd` | — | sì (presente) | no |
| Fai avanzare a più recente | `AdvanceToLatestCmd` | — | sì (presente) | — |
| Cronologia | `ShowHistoryCmd` | — | sì (presente) | no |
| Interrompi collegamento | `BreakXRefLinkCmd` | `Occurrence.breakLink` | sì (presente) | no |
| Sostituisci componente | `FusionComponentReplaceCommand` | `Occurrence.replace` | sì (presente) | sì |
| Copia | `CopyCommand` | `BRepBody.copyToComponent` | sì (presente) | no |
| Taglia | `CutCommand` | — | sì (presente) | — |
| Incolla | `PasteCommand` | `Occurrences.addNewComponentCopy` | sì (presente) | no |
| Incolla nuovo | `FusionPasteNewCommand` | `Documents.add` | sì (presente) | sì |
| Esporta DXF | `SketchExportToDXFCommand` | `Documents.add` | sì (presente) | sì |
| Elimina tutte le lavorazioni da Contrassegno cronologia | `FusionTrimFeaturesCommand` | `TrimFeatures` | sì (presente) | no |
| SurfaceShellDeleteCommand | `SurfaceShellDeleteCommand` | `ShellFeatures` | sì (presente) | sì |
| Rinomina | `RenameBrowserCmd` | `Component.name` | sì (presente) | sì |
| Vista su faccia o piano | `LookAtCommand` | `Viewport.camera` | sì (presente) | sì |
| Controllo dettaglio visualizzazione | `TessellationControlCmd` | — | sì (presente) | — |
| Mostra profilo | `ShowProfile` | — | sì (presente) | no |
| Nascondi profilo | `HideProfile` | — | sì (presente) | no |
| Mostra quota | `ShowDimension` | — | sì (presente) | no |
| Nascondi quote | `HideDimension` | — | sì (presente) | no |
| Mostra geometrie proiettate | `ShowProjectedGeometries` | — | sì (presente) | no |
| Nascondi geometrie proiettate | `HideProjectedGeometries` | — | sì (presente) | no |
| Mostra geometrie di costruzione | `ShowConstructionGeometries` | — | sì (presente) | no |
| Nascondi geometrie di costruzione | `HideConstructionGeometries` | — | sì (presente) | no |
| Mostra/Nascondi | `VisibilityToggleCmd` | `Occurrence.isLightBulbOn` | sì (presente) | sì |
| Mostra tutti i componenti | `ShowAllComponentsCmd` | — | sì (presente) | no |
| Mostra tutti i corpi | `ShowAllBodiesCmd` | — | sì (presente) | no |
| Mostra tutto | `ShowAllGroupMembersCmd` | — | sì (presente) | no |
| Selezionabile/Non selezionabile | `SelectabilityToggleCmd` | `Selections` | sì (presente) | no |
| Mostra/Nascondi piani | `PlanesVisibilityToggleCmd` | — | sì (presente) | no |
| Mostra/Nascondi assi | `AxesVisibilityToggleCmd` | — | sì (presente) | no |
| Mostra/Nascondi punti | `PointsVisibilityToggleCmd` | — | sì (presente) | no |
| Controllo dell'opacità | `OpacityControlCmd` | `Occurrence.visibleOpacity` | sì (presente) | sì |
| Opacità personalizzata | `CustomOpacityControlCmd` | `CustomFeatures 🧪` | sì (presente) | no |
| 10% | `OpacityCtrlTenCmd` | — | sì (presente) | — |
| 20% | `OpacityCtrlTwentyCmd` | — | sì (presente) | — |
| 30% | `OpacityCtrlThirtyCmd` | — | sì (presente) | — |
| 40% | `OpacityCtrlFortyCmd` | — | sì (presente) | — |
| 50% | `OpacityCtrlFiftyCmd` | — | sì (presente) | — |
| 60% | `OpacityCtrlSixtyCmd` | — | sì (presente) | — |
| 70% | `OpacityCtrlSeventyCmd` | — | sì (presente) | — |
| 80% | `OpacityCtrlEightyCmd` | — | sì (presente) | — |
| 90% | `OpacityCtrlNinetyCmd` | — | sì (presente) | — |
| 100% | `OpacityCtrlHundredCmd` | — | sì (presente) | — |
| Isola | `IsolateCmd` | `Occurrence.isIsolated` | sì (presente) | sì |
| Rimuovi isolamento | `UnisolateCmd` | `Occurrence.isIsolated` | sì (presente) | sì |
| Rimuovi isolamento per tutti | `UnisolateAllCmd` | `Occurrence.isIsolated` | sì (presente) | sì |
| Colore componente ciclo | `CycleComponentColorCmd` | — | sì (presente) | — |
| Trova nel browser | `FindInBrowser` | — | sì (presente) | — |
| Trova nella finestra | `FindInWindow` | — | nesting: estensione a pagamento — da verificare | — |
| Trova nella timeline | `FusionFindInTimeline` | — | sì (presente) | — |
| Passare a Modellazione parametrica | `ConvertToPMDesignCommand` | `Design.designType` | sì (presente) | sì |
| Passa a Modellazione diretta | `ConvertToDMDesignCommand` | `Design.designType` | sì (presente) | sì |
| SelectiveCreateWorkingModelFromBodyCommand | `SelectiveCreateWorkingModelFromBodyCommand` | `Selections` | sì (presente) | no |
| SelectiveCreateWorkingModelFromCompCommand | `SelectiveCreateWorkingModelFromCompCommand` | `Selections` | sì (presente) | no |
| Ignora/Mostra problemi della pila | `FastenerStackAnalysisIgnoreToggleCmd` | — | sì (presente) | no |
| Inserisci elemento di fissaggio simile | `FastenersInsertSimilar` | — | sì (presente) | — |
| Modifica elemento di fissaggio | `FastenersEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Sostituisci elemento di fissaggio | `FastenersReplaceCommand` | — | sì (presente) | — |
| Risolvi elemento di fissaggio | `ResolveFastenerCommand` | — | sì (presente) | — |
| Aggiorna automaticamente dimensioni | `FastenersStackUpdateCmd` | `FastenerOccurrenceDefinition.updateSize 🧪` | sì (presente) | no |
| Opzioni elementi di fissaggio | `FastenersOptionsCmd` | — | sì (presente) | — |
| Aggiorna automaticamente tutte le dimensioni | `FastenersAllStacksUpdateCmd` | `FastenerOccurrenceDefinition.updateSize 🧪` | sì (presente) | no |
| Modifica disposizione | `DcArrangeEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica disposizione | `DcAdvandedArrangeEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica area di disegno | `DcArrangeEditSketchCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica solido di delimitazione | `DcStockModelEditCommand` | `BoxFeatures` | sì (presente) | no |
| Modifica lavorazione | `FusionEditFeatureCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `FusionEditDcFeatureCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Dissolvi | `DissolveFeatureCmdDef` | — | sì (presente) | — |
| Modifica lavorazione  | `FusionSculptEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `BoxPrimitiveEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `CylinderPrimitiveEditCommand` | `CylinderFeatures` | sì (presente) | no |
| Modifica lavorazione | `SpherePrimitiveEditCommand` | `SphereFeatures` | sì (presente) | no |
| Modifica lavorazione  | `TorusPrimitiveEditCommand` | `TorusFeatures` | sì (presente) | no |
| Modifica lavorazione  | `PipePrimitiveEditCommand` | `PipeFeatures` | sì (presente) | sì |
| Modifica lavorazione  | `CoilPrimitiveEditCommand` | `CoilFeatures` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcFilletEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcSurfaceThickenEditCommand` | `ThickenFeatures` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcChamferEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcShellFeatureEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionExtrudeEditCommand` | `ExtrudeFeatures` | sì (presente) | sì |
| Modifica lavorazione  | `FusionSurfaceExtrudeEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionRevolveEditCommand` | `RevolveFeatures` | sì (presente) | sì |
| Modifica lavorazione  | `FusionSurfaceRevolveEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionSweepEditCommand` | `SweepFeatures` | sì (presente) | sì |
| Modifica lavorazione  | `FusionSurfaceSweepEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionCombineEditCommand` | `CombineFeatures` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcSplitBodyEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcSplitFaceEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazioni | `FusionDcReplaceFaceEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcDeleteFaceEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionDcPartingLineSplitEditCommand` | `SilhouetteSplitFeatures` | sì (presente) | no |
| Modifica piano di costruzione  | `FusionDcEditConstructionTangentPlaneCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica piano di costruzione  | `FusionDcEditConstructionPlaneFromThreePointsCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica piano di costruzione | `FusionDcEditConstructionPlanePerpendicularToPlaneCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica asse di costruzione | `FusionDcEditConstructionAxisNormalToFaceCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica punto di costruzione | `FusionDcEditConstructionPointFromThreePlanesCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica punto di costruzione | `FusionDcEditConstructionPointFromCircleOrSphereCommand` | `SketchCircles` | sì (presente) | sì |
| Modifica piano di costruzione | `FusionDcEditConstructionPlaneByPlaneOffsetCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica piano di costruzione | `FusionDcEditConstructionMidPlaneCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica piano di costruzione | `FusionDcEditConstructionPlaneFromTwoEdgesCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica piano di costruzione  | `FusionDcEditConstructionPlaneAtAngleCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica piano di costruzione | `FusionDcEditConstructionPlaneAlongPathCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica punto di costruzione | `FusionDcEditConstructionPointFromPointCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica punto di costruzione | `FusionDcEditConstructionPointAtEdgeAndPlaneCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica punto di costruzione | `FusionDcEditConstructionPointThroughTwoEdgesCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica punto di costruzione | `FusionDcEditConstructionPointAlongPathCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica asse di costruzione | `FusionDcEditConstructionAxisThroughCylinderCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica asse di costruzione | `FusionDcEditConstructionAxisFromTwoPlanesCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica asse di costruzione  | `FusionDcEditConstructionAxisThroughEdgeCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica asse di costruzione  | `FusionDcEditConstructionAxisThroughTwoPointsCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione  | `FusionOffsetFacesEditCommand` | `OffsetFacesFeatures` | sì (presente) | sì |
| Modifica | `BaseFeatureActivate` | `BaseFeatures` | sì (presente) | sì |
| Modifica | `SnapshotActivate` | `Viewport.camera` | sì (presente) | sì |
| Modifica | `TSplineBaseFeatureActivate` | `FormFeatures` | sì (presente) | sì |
| Modifica | `PCBActivate` | — | sì (presente) | — |
| Modifica flangia | `FusionBaseFaceEditCommand` | `BaseFeatures` | sì (presente) | sì |
| Modifica raccordo lamiera | `FusionSheetMetalFilletEditCommand` | `FilletFeatures` | sì (presente) | sì |
| Modifica smusso lamiera | `FusionSheetMetalChamferEditCommand` | `ChamferFeatures` | sì (presente) | sì |
| Modifica Chiusura angolo | `FusionCornerEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica Unisci per piega | `FusionJoinByBendEditCommand` | `JoinByBendFeatures 🧪` | sì (presente) | no |
| Modifica Piega cosmetica | `FusionSheetMetalCosmeticBendEditCmd` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica riduzione | `FusionSheetMetalJogEditCommand` | — | sì (presente) | — |
| Modifica profilo di schizzo | `FusionEditDcFeatureProfileCommand` | — | sì (presente) | — |
| Modifica profilo di schizzo | `ProfileSketchActivate` | — | sì (presente) | — |
| Modifica spiegatura | `SheetmetalEditUnfoldCommand` | `UnfoldFeatures` | sì (presente) | sì |
| Modifica piega | `SheetMetalFoldEditCmd` | `FoldFeatures 🧪` | sì (presente) | no |
| Modifica Converti in lamiera | `ConvertToSheetMetalEditCmd` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica separazione | `SheetMetalRipEditCmd` | `RipFeatures` | sì (presente) | no |
| Modifica lavorazione | `APIFeatureEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione derivata | `EditDeriveCommand` | `DeriveFeatures` | sì (presente) | sì |
| Interrompi collegamento | `BreakExternalDeriveLinkCmd` | `DeriveFeature.breakLink` | sì (presente) | no |
| Modifica lavorazione  | `FusionAutomatedModelingEditCommand` | `TimelineObject.rollTo` | modellazione automatica / generativa: no | sì |
| Configura | `ConfigureEntityCmd` | — | configurazioni: no | — |
| Configura | `ConfigureFeatureCmd` | — | configurazioni: no | — |
| Espandi gruppo | `FusionExpandGroupFeatureCommand` | — | sì (presente) | — |
| Crea gruppo | `FusionCreateGroupFeatureCommand` | `TimelineGroups.add` | sì (presente) | sì |
| BaseFeatureCreation | `BaseFeatureCreation` | `BaseFeatures` | sì (presente) | sì |
| TSplineBaseFeatureCreation | `TSplineBaseFeatureCreation` | `FormFeatures` | sì (presente) | sì |
| Interrompi collegamento | `BreakWorkingModelLinkCmd` | — | sì (presente) | — |
| Rinomina | `FusionRenameTimelineEntryCommand` | `TimelineObject.name` | sì (presente) | sì |
| RollToEndCommand | `RollToEndCommand` | `Timeline.moveToEnd` | sì (presente) | sì |
| Scorrimento contrassegno timeline qui | `FusionRollCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Converti in lavorazione MD | `ConvertToDMFeatureCommand` | — | sì (presente) | — |
| Converti in Parametrica | `ConvertToPMFeatureCommand` | — | sì (presente) | — |
| Sopprimi lavorazioni | `FusionSuppressCommand` | `TimelineObject.isSuppressed` | sì (presente) | sì |
| Scopri lavorazioni | `FusionUnsuppressCommand` | `TimelineObject.isSuppressed` | sì (presente) | sì |
| Attiva configurazione | `DesignConfigurationActivateRowCmd` | — | configurazioni: no | — |
| Aggiungi configurazione | `DesignConfigurationAddRowCmd` | — | configurazioni: no | — |
| Elimina configurazione | `DesignConfigurationDeleteRowCmd` | — | configurazioni: no | — |
| Copia in nuova configurazione | `DesignConfigurationCopyRowCmd` | — | configurazioni: no | — |
| Esamina avvertimento | `FusionLookupErrInfoCommand` | — | sì (presente) | — |
| Rimuovi sostituzioni visibilità | `RemoveVisibilityOverridesCommand` | `RemoveFeatures` | sì (presente) | no |
| FusionDesignAdviceFindInTable | `FusionDesignAdviceFindInTable` | — | sì (presente) | — |
| Modifica unità attive | `FusionChangeActiveUnitsCommand` | `FusionUnitsManager.distanceDisplayUnits` | sì (presente) | sì |
| Modifica tipo di progettazione | `FusionChangeDesignDocTypeCmd` | `Design.designType` | sì (presente) | sì |
| Elemento Shell superficie media | `FusionSurfaceMidsurfaceShellCommand` | — | sì (presente) | — |
| Shell di offset | `FusionSurfaceOffsetShellCommand` | `OffsetFeatures` | sì (presente) | no |
| Shell dalla superficie | `SurfaceShellConvertCommand` | `ShellFeatures` | sì (presente) | sì |
| Attiva/disattiva raggio | `ToggleRadialDimCmd` | — | sì (presente) | no |
| Attiva/disattiva diametro | `ToggleDiameterDimCmd` | — | sì (presente) | no |
| Attiva/disattiva non parametrica | `ToggleDrivenDimCmd` | — | sì (presente) | no |
| Attiva/disattiva parametrica | `ToggleDrivingDimCmd` | — | sì (presente) | no |
| ToggleMinimumTanDimCmd | `ToggleMinimumTanDimCmd` | — | sì (presente) | no |
| ToggleMaximumTanDimCmd | `ToggleMaximumTanDimCmd` | — | sì (presente) | no |
| Aggiungi quota offset | `OffsetDimensionCmd` | `OffsetFeatures` | sì (presente) | no |
| Modifica offset | `OffsetSketchEdit` | `Sketch` | sì (presente) | no |
| Modifica elemento Shell superficie media | `FusionSurfaceMidsurfaceShellEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica elemento Shell superficie | `FusionSurfaceShellEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| MeshDeleteTrianglesCommand | `MeshDeleteTrianglesCommand` | — | sì (presente) | — |
| Vincoli | `SketchGeomConstraintCmd` | `GeometricConstraints` | sì (presente) | sì |
| Project | `Project` | `Sketch.project` | sì (presente) | sì |
| Sposta | `FusionMoveComponentsCommand` | `MoveFeatures` | sì (presente) | sì |
| FusionCreateEmptyComponentCommand | `FusionCreateEmptyComponentCommand` | `Occurrences.addNewComponent` | sì (presente) | sì |
| FusionCreateComponentFromBodyCommand | `FusionCreateComponentFromBodyCommand` | `BRepBody.createComponent` | sì (presente) | sì |
| Ombreggiatura piatta | `ParaMeshFlatMeshShadingCommand` | — | sì (presente) | — |
| Ombreggiatura uniforme | `ParaMeshSmoothMeshShadingCommand` | — | sì (presente) | — |
| Modifica lavorazione  | `ParaMeshBaseFeatureActivateCommand` | — | sì (presente) | — |
| Modifica lavorazione | `ParaMeshDcSmoothEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcSmoothBoundaryEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcHollowEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcReduceEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcCombineEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcRepairEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcToQuadMeshEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcRemeshEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcPlaneCutEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcTessellateEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcConvertEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcExtractEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcCalculateFaceGroupsEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcMoveCopyEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcReverseNormalsEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcScaleEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcBridgeEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcMergeFaceGroupsEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcPlanarSectionEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica lavorazione | `ParaMeshDcTextureEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Rimuovi | `VolFieldRemoveModelCommand` | `VolumetricModelFeatures 🧪` | sì (presente) | no |
| Converti modello volumetrico in mesh | `VolFieldModelToMeshCommand` | `VolumetricModelFeatures 🧪` | sì (presente) | no |
| Opzioni di visualizzazione volumetrica | `VolFieldDisplayOptionsCommand` | `VolumetricModelFeatures 🧪` | sì (presente) | no |
| VolFieldDcCreateModelEditCmd | `VolFieldDcCreateModelEditCmd` | `VolumetricModelFeatures 🧪` | sì (presente) | no |
| Modifica lavorazione | `VolFieldDcSolidityOffsetEditCmd` | `VolumetricModelFeatures 🧪` | sì (presente) | no |
| Modifica lavorazione | `VolFieldDcSolidityAlongPathEditCmd` | `VolumetricModelFeatures 🧪` | sì (presente) | no |
| Modifica lavorazione | `VolFieldDcAddLatticeEditCmd` | `VolumetricModelFeatures 🧪` | sì (presente) | no |
| Modifica lavorazione | `VolFieldDcVolumetricModelEditCmd` | `VolumetricModelFeatures 🧪` | sì (presente) | no |
| Modifica lavorazione | `VolFieldDcCreateLatticeEditCmd` | `VolumetricModelFeatures 🧪` | sì (presente) | no |
| Modifica lavorazione | `VolFieldDcModelToMeshEditCmd` | `VolumetricModelFeatures 🧪` | sì (presente) | no |
| Modifica lavorazione | `VolFieldDcTextureEditCmd` | `VolumetricModelFeatures 🧪` | sì (presente) | no |

## Produzione (Manufacture, CNC) / Scheda Fresatura (`MillingTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Nuovo Setup | `CreateSetupCmd` | `Setups` | sì (presente) | sì |
| Crea programma NC | `IronNcProgram` | `NCPrograms` | sì (presente) | no |
| Nuova cartella | `IronFolder` | `CAMFolders` | sì (presente) | no |
| Nuova serie | `IronPattern` | `CAMPatterns` | sì (presente) | no |
| NC manuale | `IronStrategy_manual` | `operations.createInput("manual")` | sì (presente) | sì |
| Ispezione per WCS | `IronStrategy_probe` | `operations.createInput("probe")` | tastatore/ispezione: no | sì |
| Nuovo gruppo setup | `CreateSetupGroupCmd` | `Setups` | sì (presente) | sì |
| Orientamento utensile | `IronStrategy_tool_orientation` | `operations.createInput("tool_orientation")` | CAM 3+2 / multiasse: no | sì |
| Inserisci dati di produzione | `IronImportAllCAMXRefsCmd` | — | sì (presente) | — |
| Debug parametri oggetti CAD | `IronStrategy_debug_cad_objects` | `operations.createInput("debug_cad_objects")` | sì (presente) | sì |
| Crea modello di produzione | `MSFWmdCreateAggregationAssetWorkingModelCmd` | `ManufacturingModels` | sì (presente) | no |
| Riconoscimento lavorazione | `IronStrategy_featureRecognition` | `operations.createInput("featureRecognition")` | sì (presente) | sì |
| Sgrossatura adattiva 2D | `IronStrategy_adaptive2d` | `operations.createInput("adaptive2d")` | sì (presente) | sì |
| Sgrossatura offset 2D (tasca) | `IronStrategy_pocket2d` | `operations.createInput("pocket2d")` | sì (presente) | sì |
| Spianatura | `IronStrategy_face` | `operations.createInput("face")` | sì (presente) | sì |
| Contornatura 2D | `IronStrategy_contour2d` | `operations.createInput("contour2d")` | sì (presente) | sì |
| Asola | `IronStrategy_slot` | `operations.createInput("slot")` | sì (presente) | sì |
| Traccia | `IronStrategy_path3d` | `operations.createInput("path3d")` | sì (presente) | sì |
| Filettatura | `IronStrategy_thread` | `operations.createInput("thread")` | sì (presente) | sì |
| Fresatura elicoidale | `IronStrategy_bore` | `operations.createInput("bore")` | sì (presente) | sì |
| Circolare | `IronStrategy_circular` | `operations.createInput("circular")` | sì (presente) | sì |
| Incisione | `IronStrategy_engrave` | `operations.createInput("engrave")` | sì (presente) | sì |
| Smussatura | `IronStrategy_chamfer2d` | `operations.createInput("chamfer2d")` | sì (presente) | sì |
| Sgrossatura adattiva 3D | `IronStrategy_adaptive` | `operations.createInput("adaptive")` | sì (presente) | sì |
| Sgrossatura offset 3D (tasca) | `IronStrategy_pocket_new` | `operations.createInput("pocket_new")` | sì (presente) | sì |
| Sgrossatura 3+2 | `IronStrategy_moduleworks_three_plus_two` | `operations.createInput("moduleworks_three_plus_two")` | CAM 3+2 / multiasse: no | sì |
| Distanza di sicurezza area modello | `IronStrategy_model_area_clearance` | `operations.createInput("model_area_clearance")` | sì (presente) | sì |
| Ripido e bassa pendenza | `IronStrategy_steep_and_shallow` | `operations.createInput("steep_and_shallow")` | sì (presente) | sì |
| Piana | `IronStrategy_flat` | `operations.createInput("flat")` | sì (presente) | sì |
| Parete | `IronStrategy_inclined_walls` | `operations.createInput("inclined_walls")` | sì (presente) | sì |
| Parallelo | `IronStrategy_parallel_new` | `operations.createInput("parallel_new")` | sì (presente) | sì |
| Scallop | `IronStrategy_scallop_new` | `operations.createInput("scallop_new")` | sì (presente) | sì |
| Contornatura 3D | `IronStrategy_contour_new` | `operations.createInput("contour_new")` | sì (presente) | sì |
| Rampa | `IronStrategy_ramp` | `operations.createInput("ramp")` | sì (presente) | sì |
| Bitangenza | `IronStrategy_pencil_new` | `operations.createInput("pencil_new")` | sì (presente) | sì |
| Orizzontale | `IronStrategy_horizontal_new` | `operations.createInput("horizontal_new")` | sì (presente) | sì |
| Spirale | `IronStrategy_spiral_new` | `operations.createInput("spiral_new")` | sì (presente) | sì |
| Radiale | `IronStrategy_radial_new` | `operations.createInput("radial_new")` | sì (presente) | sì |
| Spirale con morphing | `IronStrategy_morphed_spiral` | `operations.createInput("morphed_spiral")` | sì (presente) | sì |
| Proiezione | `IronStrategy_project` | `operations.createInput("project")` | sì (presente) | sì |
| Blend | `IronStrategy_blend` | `operations.createInput("blend")` | sì (presente) | sì |
| Morphing | `IronStrategy_morph` | `operations.createInput("morph")` | sì (presente) | sì |
| Angolo | `IronStrategy_rest_finishing` | `operations.createInput("rest_finishing")` | sì (presente) | sì |
| Flusso (obsoleto) | `IronStrategy_flow` | `operations.createInput("flow")` | sì (presente) | sì |
| Flow | `IronStrategy_flow2` | `operations.createInput("flow2")` | sì (presente) | sì |
| Smusso 3D | `IronStrategy_chamfer` | `operations.createInput("chamfer")` | sì (presente) | sì |
| Sbavatura | `IronStrategy_moduleworks_automatic_deburring` | `operations.createInput("moduleworks_automatic_deburring")` | sì (presente) | sì |
| Geodetica | `IronStrategy_moduleworks_geodesic` | `operations.createInput("moduleworks_geodesic")` | sì (presente) | sì |
| Punta | `IronStrategy_drill` | `operations.createInput("drill")` | sì (presente) | sì |
| Riconoscimento fori | `IronHoleRecognition` | `CAMHoleRecognition` | sì (presente) | no |
| Gestione fori | `IronHoleManager` | `CAMHoleRecognition` | sì (presente) | no |
| Lavorazione fori | `IronMachineHoles` | `CAMHoleRecognition` | sì (presente) | no |
| Sgrossatura offset rotativa (tasca) | `IronStrategy_moduleworks_4axis_roughing` | `operations.createInput("moduleworks_4axis_roughing")` | sì (presente) | sì |
| Sgrossatura multi-asse | `IronStrategy_moduleworks_multiaxis_roughing` | `operations.createInput("moduleworks_multiaxis_roughing")` | CAM 3+2 / multiasse: no | sì |
| Swarf | `IronStrategy_swarf5d` | `operations.createInput("swarf5d")` | CAM 3+2 / multiasse: no | sì |
| Swarf avanzato | `IronStrategy_moduleworks_swarf` | `operations.createInput("moduleworks_swarf")` | CAM 3+2 / multiasse: no | sì |
| Contornatura multi-asse | `IronStrategy_multiAxisContour` | `operations.createInput("multiAxisContour")` | CAM 3+2 / multiasse: no | sì |
| Rotazione parallela | `IronStrategy_rotary_finishing` | `operations.createInput("rotary_finishing")` | CAM 3+2 / multiasse: no | sì |
| Contornatura rotativa | `IronStrategy_moduleworks_4axis_finishing` | `operations.createInput("moduleworks_4axis_finishing")` | sì (presente) | sì |
| Finitura multi-asse | `IronStrategy_moduleworks_multiaxis_finishing` | `operations.createInput("moduleworks_multiaxis_finishing")` | CAM 3+2 / multiasse: no | sì |
| CAM automatizzato | `IronAutomatedCAM` | `MachiningPlan 🧪` | sì (presente) | no |
| Ritaglia | `IronToolpathTrim` | — | sì (presente) | — |
| Elimina passate | `IronToolpathEditDelete` | — | sì (presente) | — |
| Passi e collegamenti | `IronToolpathEditLeadsLinks` | — | sì (presente) | — |
| Sostituisci utensile | `IronToolpathEditToolChange` | — | sì (presente) | — |
| Sposta posizioni di ingresso | `IronToolpathEditMoveStartPoints` | — | sì (presente) | — |
| Velocità di avanzamento | `IronToolpathEditFeedrate` | — | sì (presente) | — |
| Genera | `IronGenerateToolpath` | `CAM.generateToolpath` | sì (presente) | sì |
| Simula | `IronSimulation` | — | sì (presente) | — |
| Simula con la macchina | `IronMachineSimulation` | — | sì (presente) | — |
| Post processa | `IronPostProcess` | `CAM.postProcess` | sì (presente) | sì |
| Foglio di lavoro | `IronSetupSheetSwitchboard` | `CAM` | sì (presente) | sì |
| Tempo di lavorazione | `IronMachiningTime` | `CAM.getMachiningTime` | sì (presente) | sì |
| Fresa di forma | `IronStrategy_create_form_mill` | `operations.createInput("create_form_mill")` | sì (presente) | sì |
| Pinza utensile di tornitura | `IronTurningToolHolder` | `TurningTool.holderGeometry` | sì (presente) | no |
| Portautensile | `IronToolBlock` | `ToolBlock` | sì (presente) | no |
| Pinza utensile di fresatura | `IronStrategy_SolidHolderMilling` | `operations.createInput("SolidHolderMilling")` | sì (presente) | sì |
| Librerie utensili | `IronToolLibrary` | `DocumentToolLibrary` | sì (presente) | sì |
| Libreria materiali grezzi | `IronStockMaterialLibrary` | `DocumentStockMaterialLibrary` | sì (presente) | no |
| Libreria macchine | `IronMachineLibrary` | `MachineLibrary` | sì (presente) | no |
| Libreria post | `IronPostLibrary` | `PostLibrary` | sì (presente) | sì |
| Libreria Template | `IronTemplateLibrary` | `CAMTemplateLibrary` | sì (presente) | no |
| Configurazione fogli di lavoro | `IronSetupSheetConfigurations` | `CAM.generateSetupSheet` | sì (presente) | no |
| Gestione attività | `IronTaskManager` | — | sì (presente) | — |
| Esporta valori di default | `IronExportDefaults` | — | sì (presente) | — |
| Importa valori di default | `IronImportDefaults` | — | sì (presente) | — |
| Ripristina valori di default | `IronResetDefaults` | — | sì (presente) | — |
| Barra di selezione | `AdvancedDirectSelectionIronParam` | `Selections` | sì (presente) | no |

## Produzione (Manufacture, CNC) / Scheda Tornitura (`TurningTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Tornitura - Faccia | `IronStrategy_turningFace` | `operations.createInput("turningFace")` | sì (presente) | sì |
| Tornitura - Sgrossatura profilo | `IronStrategy_turningProfileRoughing` | `operations.createInput("turningProfileRoughing")` | sì (presente) | sì |
| Tornitura - Finitura profilo | `IronStrategy_turningProfileFinishing` | `operations.createInput("turningProfileFinishing")` | sì (presente) | sì |
| Tornitura - Sgrossatura gola | `IronStrategy_turningGrooveRoughing` | `operations.createInput("turningGrooveRoughing")` | sì (presente) | sì |
| Finitura tornitura gola | `IronStrategy_turningGrooveFinishing` | `operations.createInput("turningGrooveFinishing")` | sì (presente) | sì |
| Tornitura - Profilatura | `IronStrategy_turningRoughing` | `operations.createInput("turningRoughing")` | sì (presente) | sì |
| Tornitura - Sgrossatura adattiva | `IronStrategy_turningAdaptiveRoughing` | `operations.createInput("turningAdaptiveRoughing")` | sì (presente) | sì |
| Tornitura - Gola | `IronStrategy_turningProfileGroove` | `operations.createInput("turningProfileGroove")` | sì (presente) | sì |
| Tornitura - Gola singola | `IronStrategy_turningGroove` | `operations.createInput("turningGroove")` | sì (presente) | sì |
| Tornitura - Filetto | `IronStrategy_turningThread` | `operations.createInput("turningThread")` | sì (presente) | sì |
| Tornitura - Smusso | `IronStrategy_turningChamfer` | `operations.createInput("turningChamfer")` | sì (presente) | sì |
| Tornitura - Taglio | `IronStrategy_turningPart` | `operations.createInput("turningPart")` | sì (presente) | sì |
| Tornitura - Traccia | `IronStrategy_turningTrace` | `operations.createInput("turningTrace")` | sì (presente) | sì |
| Presa contromandrino | `IronStrategy_turningSecondarySpindleGrab` | `operations.createInput("turningSecondarySpindleGrab")` | sì (presente) | sì |
| Estrazione barra | `IronStrategy_turningSecondarySpindlePull` | `operations.createInput("turningSecondarySpindlePull")` | sì (presente) | sì |
| Ritorno contromandrino | `IronStrategy_turningSecondarySpindleReturn` | `operations.createInput("turningSecondarySpindleReturn")` | sì (presente) | sì |
| Chiamata utensile | `IronStrategy_turningToolCall` | `operations.createInput("turningToolCall")` | sì (presente) | sì |

## Produzione (Manufacture, CNC) / Scheda Additivo (`AdditiveTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Nuovo setup da G-Code | `IronAdditiveImportGCode` | — | sì (presente) | — |
| Sposta componenti | `CAMMoveComponentsCommand` | — | sì (presente) | — |
| Altezza minima costruzione | `IronMinimizeBoundingBox` | — | sì (presente) | — |
| Orientamento automatico | `IronStrategy_additive_optimize_orientation` | `operations.createInput("additive_optimize_orientation")` | sì (presente) | sì |
| Disponi | `IronStrategy_additive_arrange_strategy` | `operations.createInput("additive_arrange_strategy")` | sì (presente) | sì |
| Gruppo di subnest | `IronStrategy_additive_subnest_strategy` | `operations.createInput("additive_subnest_strategy")` | nesting: estensione a pagamento — da verificare | sì |
| Posiziona su piattaforma | `IronPlaceOnPlatform` | — | sì (presente) | — |
| Analisi interferenze | `IronStrategy_additive_interference_analysis` | `operations.createInput("additive_interference_analysis")` | sì (presente) | sì |
| Volume di costruzione di riempimento | `FillPlatformCmd` | — | sì (presente) | — |
| Duplica | `LinearArrangeCmd` | — | sì (presente) | — |
| Assegna preset corpo | `IronAssignBuildStrategy` | `AdditiveSetupUtility.assignPartsToBodyPreset` | sì (presente) | no |
| Dividi supporti | `SplitSupportCmd` | `AdditiveSetupUtility.splitSupport` | sì (presente) | no |
| Rimuovi componenti | `RemoveExcessParts` | `AdditiveSetupUtility.removeExcessParts` | sì (presente) | no |
| Supporto volumetrico | `IronStrategy_areavolume_additive_support` | `operations.createInput("areavolume_additive_support")` | sì (presente) | sì |
| Supporto volumetrico | `IronStrategy_areavolume_additive_fff_support` | `operations.createInput("areavolume_additive_fff_support")` | sì (presente) | sì |
| Volume circostante per supporto polilinea | `IronStrategy_surroundvolumepolyline_additive_support` | `operations.createInput("surroundvolumepolyline_additive_support")` | sì (presente) | sì |
| Supporto della barra | `IronStrategy_areabar_additive_support` | `operations.createInput("areabar_additive_support")` | sì (presente) | sì |
| Supporto barra solido | `IronStrategy_areabar_additive_fff_support` | `operations.createInput("areabar_additive_fff_support")` | sì (presente) | sì |
| Supporto barra dei punti rivolta verso il basso | `IronStrategy_downoriented_additive_support` | `operations.createInput("downoriented_additive_support")` | sì (presente) | sì |
| Supporto reticolo | `IronStrategy_lattice_additive_support` | `operations.createInput("lattice_additive_support")` | sì (presente) | sì |
| Spigolo con supporto barra | `IronStrategy_edgebar_additive_support` | `operations.createInput("edgebar_additive_support")` | sì (presente) | sì |
| Supporto polilinea | `IronStrategy_areapolyline_additive_support` | `operations.createInput("areapolyline_additive_support")` | sì (presente) | sì |
| Spigolo con supporto polilinea | `IronStrategy_edgepolyline_additive_support` | `operations.createInput("edgepolyline_additive_support")` | sì (presente) | sì |
| Contornatura cluster con supporto polilinea | `IronStrategy_clustercontourpolyline_additive_support` | `operations.createInput("clustercontourpolyline_additive_support")` | sì (presente) | sì |
| Asse mediano con supporto polilinea | `IronStrategy_skeletonpolyline_additive_support` | `operations.createInput("skeletonpolyline_additive_support")` | sì (presente) | sì |
| Supporto piastra base | `IronStrategy_baseplate_additive_support` | `operations.createInput("baseplate_additive_support")` | sì (presente) | sì |
| Supporto per il setter | `IronStrategy_setter_additive_support` | `operations.createInput("setter_additive_support")` | sì (presente) | sì |
| Supporto laterale | `IronStrategy_lateral_additive_support` | `operations.createInput("lateral_additive_support")` | sì (presente) | sì |
| Elimina supporti | `IronStrategy_delete_additive_supports` | `operations.createInput("delete_additive_supports")` | sì (presente) | sì |
| Costruzione lavorazione | `IronStrategy_feature_construction` | `operations.createInput("feature_construction")` | sì (presente) | sì |
| Studio | `IronStrategy_AdditiveProcessSimulation` | `operations.createInput("AdditiveProcessSimulation")` | simulazione di processo additivo: estensione a pagamento — da verificare | sì |
| PreCheck | `IronAdditiveProcessSimPreCheck` | — | simulazione di processo additivo: estensione a pagamento — da verificare | — |
| Risolvi | `IronAdditiveProcessSimSolve` | — | simulazione di processo additivo: estensione a pagamento — da verificare | — |
| Visualizza mesh | `IronAdditiveMeshView` | — | simulazione di processo additivo: estensione a pagamento — da verificare | — |
| Visualizza risultati | `IronAdditiveResultsView` | — | simulazione di processo additivo: estensione a pagamento — da verificare | — |
| Simula percorso utensile additivo | `IronAdditiveSimulation` | — | sì (presente) | — |
| Crea file di costruzione macchina | `IronStrategy_additive_exportstrategy` | `operations.createInput("additive_exportstrategy")` | sì (presente) | sì |
| Crea file di costruzione macchina | `IronStrategy_additive_formlabs_exportstrategy` | `operations.createInput("additive_formlabs_exportstrategy")` | sì (presente) | sì |
| Stampa statistiche | `IronAdditiveShowPrintStatistics` | — | sì (presente) | — |
| Statistiche piattaforma | `IronAdditiveShow3DPackingDensity` | — | sì (presente) | — |
| Analisi delle sezioni | `IronAdditiveSliceStatistics` | — | sì (presente) | — |
| Esportazione scena 3MF | `IronStrategy_additive_3mf_exportstrategy` | `operations.createInput("additive_3mf_exportstrategy")` | sì (presente) | sì |
| Libreria impostazioni di stampa | `IronPrintSettingLibrary` | `PrintSettingLibrary` | sì (presente) | no |

## Produzione (Manufacture, CNC) / Scheda Risultati (`AdditiveResultsTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Attiva/disattiva spigoli elemento | `IronAdditiveProcessSimToggleEdges` | — | simulazione di processo additivo: estensione a pagamento — da verificare | — |
| Attiva/disattiva punti di indagine min/max | `IronAdditiveProcessSimMinMaxProbe` | — | simulazione di processo additivo: estensione a pagamento — da verificare | — |
| Apri cartella risultati | `IronAdditiveOpenResultsFolder` | — | simulazione di processo additivo: estensione a pagamento — da verificare | — |
| Esportazione compensata | `IronAdditiveExportCompensated` | — | simulazione di processo additivo: estensione a pagamento — da verificare | — |
| Esporta STL compensato | `IronAdditiveExportCompensatedSTL` | — | simulazione di processo additivo: estensione a pagamento — da verificare | — |
| Esporta STL deformato | `IronAdditiveExportWarpedSTL` | — | simulazione di processo additivo: estensione a pagamento — da verificare | — |
| Esporta 3MF a colori | `IronAdditiveExportColor3MF` | `CAM3MFExportOptions` | sì (presente) | no |
| Termina risultati | `AdditiveResultsStop` | — | sì (presente) | — |

## Produzione (Manufacture, CNC) / Scheda Ispezione (`ProbingTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Geometria ispezione | `IronStrategy_probe_geometry` | `operations.createInput("probe_geometry")` | tastatore/ispezione: no | sì |
| Ispezione superficie | `IronStrategy_inspectSurface` | `operations.createInput("inspectSurface")` | tastatore/ispezione: no | sì |
| Crea piano di ispezione | `IronCreateInspectionPlan` | — | sì (presente) | — |
| Allineamento parte | `PartAlignmentStart_Delayed` | — | tastatore/ispezione: no | — |
| Allineamento parte in tempo reale | `PartAlignmentStart_Live` | — | tastatore/ispezione: no | — |
| Setup ispezione CMM | `IronStrategy_cmm_inspection_setup` | `operations.createInput("cmm_inspection_setup")` | sì (presente) | sì |
| Allinea CAD alla parte | `IronStrategy_datum` | `operations.createInput("datum")` | sì (presente) | sì |
| Ispeziona manualmente superficie | `MeasureSurface` | — | sì (presente) | — |
| Scansione superficie | `ScanSurface` | — | sì (presente) | — |
| Crea ispezione manuale | `IronCreateInspections` | — | sì (presente) | — |
| Registra ispezione manuale | `IronRecordManualMeasure` | — | sì (presente) | — |
| Importa risultati di ispezione | `ImportResults` | — | sì (presente) | — |
| Connessione in tempo reale | `LiveProbing` | — | tastatore/ispezione: no | — |
| Rapporto di ispezione | `IronInspectionReport` | — | sì (presente) | — |

## Produzione (Manufacture, CNC) / Scheda Fabbricazione (`FabricationTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Origini componenti | `MSFWmdComponentLibraryCmd` | — | sì (presente) | — |
| Crea studio nest | `MSFNestPrepareNestCmd` | — | nesting: estensione a pagamento — da verificare | — |
| Genera | `MSF.MAGNestCalculateCmd.Generate` | — | nesting: estensione a pagamento — da verificare | — |
| Profilo 2D | `IronStrategy_jet2d` | `operations.createInput("jet2d")` | sì (presente) | sì |
| Libreria dei materiali del processo | `MSF.MAGMatLibraryCmd.FusionNesting` | — | nesting: estensione a pagamento — da verificare | — |
| Preset per materiale e formato | `MSF.MSFNestSaveContainerDataCmd.Create` | — | nesting: estensione a pagamento — da verificare | — |
| Denominazione automatica | `MSFNestNameConventionCmd` | — | nesting: estensione a pagamento — da verificare | — |

## Produzione (Manufacture, CNC) / Scheda Utilità (`UtilitiesTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Generazione automatica materiale grezzo in lavorazione | `IronAutomaticIPSGeneration` | — | sì (presente) | — |
| Cancella cache materiale grezzo in lavorazione | `IronClearIPSCache` | — | sì (presente) | — |
| Genera IPS GPU in base al setup | `IronGPU_IPSTest` | — | sì (presente) | — |

## Produzione (Manufacture, CNC) / Scheda Allineamento parte (`PartAlignmentTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Modifica allineamento | `PartAlignment_EditAlignment` | — | tastatore/ispezione: no | — |
| Ispezione superficie | `PartAlignment_IronStrategy_inspectSurface` | — | tastatore/ispezione: no | — |
| Post per allineamento | `PartAlignment_IronNcProgram` | — | tastatore/ispezione: no | — |
| Importa risultati di ispezione | `PartAlignment_ImportResults` | — | tastatore/ispezione: no | — |
| Mostra informazioni di allineamento parte | `PartAlignment_IronPartAlignmentInfo` | — | tastatore/ispezione: no | — |
| Mostra risultati | `PartAlignment_IronShowResults` | — | tastatore/ispezione: no | — |
| Post con allineamento | `PartAlignmentPostStop` | — | tastatore/ispezione: no | — |
| Allineamento parte di uscita | `PartAlignmentStop_Delayed` | — | tastatore/ispezione: no | — |

## Produzione (Manufacture, CNC) / Scheda Allineamento parte in tempo reale (`LiveAlignmentTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Post per allineamento in tempo reale | `PartAlignmentPostLive` | — | tastatore/ispezione: no | — |
| Connessione in tempo reale | `LivePartAlignment` | — | tastatore/ispezione: no | — |
| Esci da Allineamento parte in tempo reale | `PartAlignmentStop_Live` | — | tastatore/ispezione: no | — |

## Produzione (Manufacture, CNC) / Scheda Simulazione (`SimulationTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Pinza | `SimulationShowToolHolder` | — | sì (presente) | — |
| Gambo | `SimulationShowToolShaft` | — | sì (presente) | — |
| Tagliente | `SimulationShowToolFlute` | — | sì (presente) | — |
| Nascondi utensile | `SimulationHideTool` | — | sì (presente) | — |
| Macchina | `SimulationShowHideMachine` | — | sì (presente) | — |
| Percorsi utensile | `SimulationShowHideToolpath` | — | sì (presente) | — |
| Materiale grezzo | `SimulationShowHideStock` | — | sì (presente) | — |
| Problemi | `SimulationIssues` | — | sì (presente) | — |
| Codice NC | `SimulationNCCode` | — | sì (presente) | — |
| Materiale grezzo da modellare | `SimulationStockToModel` | — | sì (presente) | — |
| Simula più rapidamente (GPU) | `ToggleSimulationEngine` | — | sì (presente) | — |
| Esci dalla simulazione | `SimulationStop` | — | sì (presente) | — |

## Produzione (Manufacture, CNC) / Scheda menu (File, barre fisse, tasto destro, radiale) (`Menu`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| FusionDcEditWorkPlaneAlongPathCommand | `FusionDcEditWorkPlaneAlongPathCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkAxisThroughCylinderCommand | `FusionDcEditWorkAxisThroughCylinderCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkAxisFromLineCommand | `FusionDcEditWorkAxisFromLineCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkAxisFromTwoPointsCommand | `FusionDcEditWorkAxisFromTwoPointsCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkAxisFromTwoPlanesCommand | `FusionDcEditWorkAxisFromTwoPlanesCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkAxisNormalToFaceCommand | `FusionDcEditWorkAxisNormalToFaceCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Importa | `NeuCAMImportCommand` | `ImportManager` | sì (presente) | sì |
| Modifica | `IronEditOperation` | `Operation.parameters` | sì (presente) | sì |
| Modifica ispezioni manuali | `IronEditInspections` | — | sì (presente) | — |
| Modifica modello di produzione per Setup | `IronEditWorkingModelSetup` | — | sì (presente) | — |
| Modifica | `IronAdditiveEditPrintSetting` | `Documents.add` | sì (presente) | sì |
| Modifica | `IronEditHoleRecognition` | — | sì (presente) | — |
| Modifica | `IronEditMachineHoles` | — | sì (presente) | — |
| Modifica | `IronEditNcProgram` | `NCProgram` | sì (presente) | no |
| Modifica utensile | `IronEditTool` | `Tool` | sì (presente) | sì |
| Modifica segno foro | `IronEditHoleSignature` | — | sì (presente) | — |
| Confronta e modifica | `IronCompareAndEdit` | `TimelineObject.rollTo` | sì (presente) | sì |
| IronCompareAndEditRework | `IronCompareAndEditRework` | — | sì (presente) | — |
| Nuovo supporto | `IronAdditiveSupport` | — | sì (presente) | — |
| Nuovo studio | `IronAdditiveOrientations` | — | sì (presente) | — |
| Modifica | `IronEditAdditiveProcessSimulation` | — | simulazione di processo additivo: estensione a pagamento — da verificare | — |
| Genera mesh | `IronAdditiveProcessSimMesh` | — | simulazione di processo additivo: estensione a pagamento — da verificare | — |
| Cancella risultati della risoluzione | `IronAdditiveDeleteProcSimResults` | — | sì (presente) | — |
| Nuova operazione | `IronNewOperation` | `Documents.add` | sì (presente) | sì |
| Foratura | `IronDrilling` | — | sì (presente) | — |
| Fresatura 2D | `Iron2DMilling` | — | sì (presente) | — |
| Fresatura 3D | `Iron3DMilling` | — | sì (presente) | — |
| Fresatura multi-asse | `IronMultiAxisMilling` | — | CAM 3+2 / multiasse: no | — |
| Tornitura | `IronTurning` | — | sì (presente) | — |
| Gestione parte | `IronPartHandling` | — | sì (presente) | — |
| Trasferimento di materiale grezzo tornitura | `IronStrategy_turningStockTransfer` | `operations.createInput("turningStockTransfer")` | sì (presente) | sì |
| Taglio | `IronWLPC` | — | sì (presente) | — |
| Ispezione | `IronInspection` | — | sì (presente) | — |
| IronStrategy_inspectSurfaceGeometry | `IronStrategy_inspectSurfaceGeometry` | `operations.createInput("inspectSurfaceGeometry")` | tastatore/ispezione: no | sì |
| Crea da modello | `IronCreateFromTemplate` | `Setup.createFromCAMTemplate` | sì (presente) | no |
| Gruppo | `IronGroupEditObjects` | `CAMFolders` | sì (presente) | no |
| Separa | `IronUngroupEditObjects` | — | sì (presente) | — |
| Mostra informazioni di allineamento parte | `IronPartAlignmentInfo` | — | tastatore/ispezione: no | — |
| Ripristino allineamento parte | `IronResetPartAlignment` | — | tastatore/ispezione: no | — |
| Misura allineamento | `MeasureDatum` | — | sì (presente) | — |
| Iron3MFExport | `Iron3MFExport` | `Documents.add` | sì (presente) | sì |
| Apri cartella di output NC | `IronOpenNcFolder` | `Documents.add` | sì (presente) | sì |
| Cancella percorso utensile | `IronClearToolpath` | `CAM.clearToolpath` | sì (presente) | no |
| Mostra | `IronDrawAllToolpathOps` | — | sì (presente) | — |
| Nascondi | `IronUndrawAllToolpathOps` | — | sì (presente) | — |
| Mostra tutto | `IronDrawAllToolpathsInParent` | — | sì (presente) | — |
| Nascondi tutto | `IronUndrawAllToolpathsInParent` | — | sì (presente) | — |
| Mostra/Nascondi percorso utensile | `IronToolpathVisibilityToggle` | — | sì (presente) | no |
| Salva parametri come default | `IronMakeAllDefault` | — | sì (presente) | — |
| Sopprimi | `IronSuppress` | `OperationBase.isSuppressed` | sì (presente) | sì |
| Proteggi | `IronProtect` | `OperationBase.isProtected` | sì (presente) | no |
| Opzionale | `IronOptional` | `OperationBase.isOptional` | sì (presente) | no |
| Modifica note | `IronEditNotes` | `OperationBase.notes` | sì (presente) | no |
| Crea operazione derivata | `IronDerivedOperation` | `DeriveFeatures` | sì (presente) | sì |
| Foratura | `IronDrilling_derived` | — | sì (presente) | — |
| Punta | `IronStrategy_drill_derived` | `operations.createInput("drill_derived")` | sì (presente) | sì |
| Fresatura 2D | `Iron2DMilling_derived` | — | sì (presente) | — |
| Spianatura | `IronStrategy_face_derived` | `operations.createInput("face_derived")` | sì (presente) | sì |
| Sgrossatura adattiva 2D | `IronStrategy_adaptive2d_derived` | `operations.createInput("adaptive2d_derived")` | sì (presente) | sì |
| Sgrossatura offset 2D (tasca) | `IronStrategy_pocket2d_derived` | `operations.createInput("pocket2d_derived")` | sì (presente) | sì |
| Contornatura 2D | `IronStrategy_contour2d_derived` | `operations.createInput("contour2d_derived")` | sì (presente) | sì |
| Asola | `IronStrategy_slot_derived` | `operations.createInput("slot_derived")` | sì (presente) | sì |
| Circolare | `IronStrategy_circular_derived` | `operations.createInput("circular_derived")` | sì (presente) | sì |
| Fresatura elicoidale | `IronStrategy_bore_derived` | `operations.createInput("bore_derived")` | sì (presente) | sì |
| Filettatura | `IronStrategy_thread_derived` | `operations.createInput("thread_derived")` | sì (presente) | sì |
| Traccia | `IronStrategy_path3d_derived` | `operations.createInput("path3d_derived")` | sì (presente) | sì |
| Incisione | `IronStrategy_engrave_derived` | `operations.createInput("engrave_derived")` | sì (presente) | sì |
| Smussatura | `IronStrategy_chamfer2d_derived` | `operations.createInput("chamfer2d_derived")` | sì (presente) | sì |
| Fresatura 3D | `Iron3DMilling_derived` | — | sì (presente) | — |
| Sgrossatura adattiva 3D | `IronStrategy_adaptive_derived` | `operations.createInput("adaptive_derived")` | sì (presente) | sì |
| Sgrossatura offset 3D (tasca) | `IronStrategy_pocket_new_derived` | `operations.createInput("pocket_new_derived")` | sì (presente) | sì |
| Sgrossatura 3+2 | `IronStrategy_moduleworks_three_plus_two_derived` | `operations.createInput("moduleworks_three_plus_two_derived")` | CAM 3+2 / multiasse: no | sì |
| Distanza di sicurezza area modello | `IronStrategy_model_area_clearance_derived` | `operations.createInput("model_area_clearance_derived")` | sì (presente) | sì |
| Parallelo | `IronStrategy_parallel_new_derived` | `operations.createInput("parallel_new_derived")` | sì (presente) | sì |
| Contornatura 3D | `IronStrategy_contour_new_derived` | `operations.createInput("contour_new_derived")` | sì (presente) | sì |
| Rampa | `IronStrategy_ramp_derived` | `operations.createInput("ramp_derived")` | sì (presente) | sì |
| Orizzontale | `IronStrategy_horizontal_new_derived` | `operations.createInput("horizontal_new_derived")` | sì (presente) | sì |
| Bitangenza | `IronStrategy_pencil_new_derived` | `operations.createInput("pencil_new_derived")` | sì (presente) | sì |
| Scallop | `IronStrategy_scallop_new_derived` | `operations.createInput("scallop_new_derived")` | sì (presente) | sì |
| Spirale | `IronStrategy_spiral_new_derived` | `operations.createInput("spiral_new_derived")` | sì (presente) | sì |
| Radiale | `IronStrategy_radial_new_derived` | `operations.createInput("radial_new_derived")` | sì (presente) | sì |
| Spirale con morphing | `IronStrategy_morphed_spiral_derived` | `operations.createInput("morphed_spiral_derived")` | sì (presente) | sì |
| Proiezione | `IronStrategy_project_derived` | `operations.createInput("project_derived")` | sì (presente) | sì |
| Blend | `IronStrategy_blend_derived` | `operations.createInput("blend_derived")` | sì (presente) | sì |
| Morphing | `IronStrategy_morph_derived` | `operations.createInput("morph_derived")` | sì (presente) | sì |
| Flusso (obsoleto) | `IronStrategy_flow_derived` | `operations.createInput("flow_derived")` | sì (presente) | sì |
| Flow | `IronStrategy_flow2_derived` | `operations.createInput("flow2_derived")` | sì (presente) | sì |
| Ripido e bassa pendenza | `IronStrategy_steep_and_shallow_derived` | `operations.createInput("steep_and_shallow_derived")` | sì (presente) | sì |
| Piana | `IronStrategy_flat_derived` | `operations.createInput("flat_derived")` | sì (presente) | sì |
| Parete | `IronStrategy_inclined_walls_derived` | `operations.createInput("inclined_walls_derived")` | sì (presente) | sì |
| Angolo | `IronStrategy_rest_finishing_derived` | `operations.createInput("rest_finishing_derived")` | sì (presente) | sì |
| Sbavatura | `IronStrategy_moduleworks_automatic_deburring_derived` | `operations.createInput("moduleworks_automatic_deburring_derived")` | sì (presente) | sì |
| Geodetica | `IronStrategy_moduleworks_geodesic_derived` | `operations.createInput("moduleworks_geodesic_derived")` | sì (presente) | sì |
| Fresatura multi-asse | `IronMultiAxisMilling_derived` | — | CAM 3+2 / multiasse: no | — |
| Sgrossatura offset rotativa (tasca) | `IronStrategy_moduleworks_4axis_roughing_derived` | `operations.createInput("moduleworks_4axis_roughing_derived")` | sì (presente) | sì |
| Sgrossatura multi-asse | `IronStrategy_moduleworks_multiaxis_roughing_derived` | `operations.createInput("moduleworks_multiaxis_roughing_derived")` | CAM 3+2 / multiasse: no | sì |
| Swarf | `IronStrategy_swarf5d_derived` | `operations.createInput("swarf5d_derived")` | CAM 3+2 / multiasse: no | sì |
| Swarf avanzato | `IronStrategy_moduleworks_swarf_derived` | `operations.createInput("moduleworks_swarf_derived")` | CAM 3+2 / multiasse: no | sì |
| Contornatura multi-asse | `IronStrategy_multiAxisContour_derived` | `operations.createInput("multiAxisContour_derived")` | CAM 3+2 / multiasse: no | sì |
| Rotazione parallela | `IronStrategy_rotary_finishing_derived` | `operations.createInput("rotary_finishing_derived")` | CAM 3+2 / multiasse: no | sì |
| Contornatura rotativa | `IronStrategy_moduleworks_4axis_finishing_derived` | `operations.createInput("moduleworks_4axis_finishing_derived")` | sì (presente) | sì |
| Finitura multi-asse | `IronStrategy_moduleworks_multiaxis_finishing_derived` | `operations.createInput("moduleworks_multiaxis_finishing_derived")` | CAM 3+2 / multiasse: no | sì |
| Tornitura | `IronTurning_derived` | — | sì (presente) | — |
| Tornitura - Sgrossatura profilo | `IronStrategy_turningProfileRoughing_derived` | `operations.createInput("turningProfileRoughing_derived")` | sì (presente) | sì |
| Tornitura - Finitura profilo | `IronStrategy_turningProfileFinishing_derived` | `operations.createInput("turningProfileFinishing_derived")` | sì (presente) | sì |
| Tornitura - Sgrossatura gola | `IronStrategy_turningGrooveRoughing_derived` | `operations.createInput("turningGrooveRoughing_derived")` | sì (presente) | sì |
| Finitura tornitura gola | `IronStrategy_turningGrooveFinishing_derived` | `operations.createInput("turningGrooveFinishing_derived")` | sì (presente) | sì |
| Tornitura - Profilatura | `IronStrategy_turningRoughing_derived` | `operations.createInput("turningRoughing_derived")` | sì (presente) | sì |
| Tornitura - Sgrossatura adattiva | `IronStrategy_turningAdaptiveRoughing_derived` | `operations.createInput("turningAdaptiveRoughing_derived")` | sì (presente) | sì |
| Tornitura - Gola | `IronStrategy_turningProfileGroove_derived` | `operations.createInput("turningProfileGroove_derived")` | sì (presente) | sì |
| Tornitura - Faccia | `IronStrategy_turningFace_derived` | `operations.createInput("turningFace_derived")` | sì (presente) | sì |
| Tornitura - Gola singola | `IronStrategy_turningGroove_derived` | `operations.createInput("turningGroove_derived")` | sì (presente) | sì |
| Tornitura - Smusso | `IronStrategy_turningChamfer_derived` | `operations.createInput("turningChamfer_derived")` | sì (presente) | sì |
| Tornitura - Taglio | `IronStrategy_turningPart_derived` | `operations.createInput("turningPart_derived")` | sì (presente) | sì |
| Tornitura - Filetto | `IronStrategy_turningThread_derived` | `operations.createInput("turningThread_derived")` | sì (presente) | sì |
| Tornitura - Traccia | `IronStrategy_turningTrace_derived` | `operations.createInput("turningTrace_derived")` | sì (presente) | sì |
| Gestione parte | `IronPartHandling_derived` | — | sì (presente) | — |
| Trasferimento di materiale grezzo tornitura | `IronStrategy_turningStockTransfer_derived` | `operations.createInput("turningStockTransfer_derived")` | sì (presente) | sì |
| Presa contromandrino | `IronStrategy_turningSecondarySpindleGrab_derived` | `operations.createInput("turningSecondarySpindleGrab_derived")` | sì (presente) | sì |
| Estrazione barra | `IronStrategy_turningSecondarySpindlePull_derived` | `operations.createInput("turningSecondarySpindlePull_derived")` | sì (presente) | sì |
| Ritorno contromandrino | `IronStrategy_turningSecondarySpindleReturn_derived` | `operations.createInput("turningSecondarySpindleReturn_derived")` | sì (presente) | sì |
| Chiamata utensile | `IronStrategy_turningToolCall_derived` | `operations.createInput("turningToolCall_derived")` | sì (presente) | sì |
| Taglio | `IronWLPC_derived` | — | sì (presente) | — |
| Profilo 2D | `IronStrategy_jet2d_derived` | `operations.createInput("jet2d_derived")` | sì (presente) | sì |
| Innalza di livello | `IronExtractEditSubToolpath` | — | sì (presente) | — |
| Modifica | `IronNewToolpathEdit` | `TimelineObject.rollTo` | sì (presente) | sì |
| Sposta qui il contrassegno | `IronMoveInsertMarkerHere` | `MoveFeatures` | sì (presente) | sì |
| Aggiungi a nuova cartella | `IronAddToNewFolder` | `Documents.add` | sì (presente) | sì |
| Aggiungi a nuovo pattern | `IronAddToNewPattern` | `Documents.add` | sì (presente) | sì |
| Duplica | `IronDuplicate` | `OperationBase.duplicate` | sì (presente) | no |
| Taglia | `IronCut` | — | sì (presente) | — |
| Copia | `IronCopy` | `OperationBase.copyAfter` | sì (presente) | no |
| Elimina | `IronDeleteObject` | `OperationBase.deleteMe` | sì (presente) | sì |
| Elimina | `IronDeleteNonIronObject` | — | sì (presente) | — |
| Elimina | `IronDeleteEditSubToolpath` | — | sì (presente) | — |
| Elimina modifiche | `IronDiscardEdits` | — | sì (presente) | — |
| Risultati orientamento | `IronAdditiveViewOrientationResults` | `Viewport.camera` | sì (presente) | sì |
| Interrompi collegamento | `IronBreakLink` | — | sì (presente) | — |
| Associa vista con nome | `IronAssociateNamedView` | `Viewport.camera` | sì (presente) | sì |
| Mostra dati percorso utensile | `IronViewToolpath` | `Viewport.camera` | sì (presente) | sì |
| Mostra registro log | `IronShowLog` | — | sì (presente) | no |
| Mostra risultati | `IronShowResults` | — | sì (presente) | no |
| Mostra rapporto | `IronAutomatedCAMShowReport` | — | sì (presente) | no |
| Modifica ispezione manuale | `IronReplayManualMeasure` | — | sì (presente) | — |
| Ricalcola risultati ispezione | `IronRecalculateInspectionResults` | — | sì (presente) | — |
| Salva come modello | `IronStoreAsTemplate` | `CAMTemplate.createFromOperations` | sì (presente) | no |
| Salva come foro modello | `IronStoreAsHoleTemplate` | — | sì (presente) | — |
| Espandi tutti i subordinati | `IronExpandAllChildren` | — | sì (presente) | — |
| Comprimi tutti i subordinati | `IronCollapseAllChildren` | — | sì (presente) | — |
| Modifica modello di produzione | `ActivateMfgWorkingModelCmd` | `ManufacturingModels` | sì (presente) | no |
| Elimina | `DeleteMfgWorkingModelCmd` | — | sì (presente) | — |
| Duplica | `DuplicateMfgWorkingModelCmd` | `ManufacturingModel.duplicate` | sì (presente) | no |
| Elimina tutti i modelli di produzione | `DeleteMfgWorkingModelsCmd` | — | sì (presente) | — |
| Crea setup dalla disposizione | `IronCreateSetupsFromArrangement` | — | sì (presente) | — |
| Crea Setup da Inviluppo | `IronCreateSetupFromEnvelope` | — | sì (presente) | — |
| Crea Setup dal modello di produzione | `IronCreateSetupFromWorkingModel` | `Setups` | sì (presente) | sì |
| Crea Setup dal modello di produzione | `IronCreateSetupsFromWorkingModel` | `Setups` | sì (presente) | sì |
| Statistiche Disposizione - Disposizione 2D | `MSFArrangeReportCmdDef` | — | sì (presente) | — |
| Statistiche Disposizione - Disposizione 3D | `Simple3dArrangeReportCmdDef` | — | sì (presente) | — |
| Statistiche Disposizione- Inviluppo 2D | `MSFEnvelopeReportCmdDef` | — | sì (presente) | — |
| Aggiornamento modelli di produzione | `IronUpdateWorkingModels` | — | sì (presente) | — |
| Mostra/nascondi linee di piega | `IronToggleBendLineVisibility` | — | sì (presente) | no |
| Modifica macchina... | `MachineBrowserEntry_EditCmd` | `TimelineObject.rollTo` | sì (presente) | sì |
| Aggiorna modello macchina | `UpdateMachineModelCmd` | — | sì (presente) | — |
| Rimuovi macchina | `MachineBrowserEntry_RemoveCmd` | — | sì (presente) | — |
| Sostituisci macchina | `MachineBrowserEntry_ReplaceCmd` | `Machine` | sì (presente) | no |
| Rimuovi dal setup | `MachineBrowserEntry_RemoveFromSetupCmd` | — | sì (presente) | — |
| Opzioni di visualizzazione raccordo geometrico | `IronResultDisplaySettings` | `Viewport.camera` | sì (presente) | sì |
| Crea gruppo di selezione | `IronCreateSelectionGroupCmd` | `Selections` | sì (presente) | no |
| Mostra/Nascondi | `CAMVisibilityToggleCmdDef` | — | sì (presente) | no |
| Mostra tutti i componenti | `CAMShowAllComponentsCmdDef` | — | sì (presente) | no |
| Mostra tutti i corpi | `CAMShowAllBodiesCmdDef` | — | sì (presente) | no |
| Isola | `IronIsolateCmd` | — | sì (presente) | no |
| Rimuovi isolamento | `IronUnisolateCmd` | — | sì (presente) | — |
| Rimuovi isolamento per tutti | `IronUnisolateAllCmd` | — | sì (presente) | — |
| Inserisci dati di produzione | `IronImportCAMXRefCmd` | `Documents.add` | sì (presente) | sì |
| Trova nel browser | `IronFindInBrowser` | — | sì (presente) | — |
| Crea elenco di taglio | `MSFNestCutListCmdDef` | — | nesting: estensione a pagamento — da verificare | — |
| WorkPlaneOffsetFromPlaneCommand | `WorkPlaneOffsetFromPlaneCommand` | — | sì (presente) | — |
| WorkAxisThroughCylinderCommand | `WorkAxisThroughCylinderCommand` | — | sì (presente) | — |
| PCBReplaceComponentCmdDef | `PCBReplaceComponentCmdDef` | — | sì (presente) | — |
| FusionDcEditWorkPlaneByPlaneOffsetCommand | `FusionDcEditWorkPlaneByPlaneOffsetCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkPlaneByLineAndAngleCommand | `FusionDcEditWorkPlaneByLineAndAngleCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkPlaneFromTwoPlanesCommand | `FusionDcEditWorkPlaneFromTwoPlanesCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkPlaneFromTwoLinesCommand | `FusionDcEditWorkPlaneFromTwoLinesCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkPlaneTangentToCylinderCommand | `FusionDcEditWorkPlaneTangentToCylinderCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkPlaneTangentToFaceAtPointCommand | `FusionDcEditWorkPlaneTangentToFaceAtPointCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkPlaneFromThreePointsCommand | `FusionDcEditWorkPlaneFromThreePointsCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkAxisFromPointAndFaceCommand | `FusionDcEditWorkAxisFromPointAndFaceCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkPointCommand | `FusionDcEditWorkPointCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkPointFromTwoLinesCommand | `FusionDcEditWorkPointFromTwoLinesCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkPointFromThreePlanesCommand | `FusionDcEditWorkPointFromThreePlanesCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkPointFromLineAndPlaneCommand | `FusionDcEditWorkPointFromLineAndPlaneCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| FusionDcEditWorkPointFromCircleOrSphereCommand | `FusionDcEditWorkPointFromCircleOrSphereCommand` | `SketchCircles` | sì (presente) | sì |
| FusionDcEditWorkPointAlongPathCommand | `FusionDcEditWorkPointAlongPathCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica | `MeshBaseFeatureActivate` | `BaseFeatures` | sì (presente) | sì |
| SheetMetalBendEditCmd | `SheetMetalBendEditCmd` | `TimelineObject.rollTo` | sì (presente) | sì |
| EditConstraintCmd | `EditConstraintCmd` | — | sì (presente) | — |
| DcEditConstraintCmd | `DcEditConstraintCmd` | `TimelineObject.rollTo` | sì (presente) | sì |
| EditAutoJointInferenceCmd | `EditAutoJointInferenceCmd` | — | sì (presente) | — |
| DcEditAutoJointInferenceCmd | `DcEditAutoJointInferenceCmd` | `TimelineObject.rollTo` | sì (presente) | sì |
| SelectJointComponentsCmd | `SelectJointComponentsCmd` | `Selections` | sì (presente) | no |
| MeshBaseFeatureCreation | `MeshBaseFeatureCreation` | `BaseFeatures` | sì (presente) | sì |
| Termina mesh | `MeshBaseFeatureStop` | `BaseFeatures` | sì (presente) | sì |
| Mesh2BRepCommand | `Mesh2BRepCommand` | `MeshConvertFeatures 🧪` | sì (presente) | sì |
| BRep2MeshCommand | `BRep2MeshCommand` | — | sì (presente) | — |
| InsertAlignMeshCommand | `InsertAlignMeshCommand` | — | sì (presente) | — |

## Disegno (Drawing) / Scheda DISEGNO (`FusionDocTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Vista di base | `FusionDrawingViewBaseCommand` | `BaseViewInput 🧪` | sì (presente) | no |
| Segnaposto vista di base | `FusionDrawingViewBaseTemplateCommand` | `BaseViewInput 🧪` | sì (presente) | no |
| Vista proiettata | `FusionDrawingViewProjectCommand` | `Views 🧪` | sì (presente) | sì |
| Segnaposto vista proiettata | `FusionDrawingViewProjectTemplateCommand` | `Views 🧪` | sì (presente) | sì |
| Vista ausiliaria | `FusionDrawingViewAuxiliaryCommand` | `Views 🧪` | sì (presente) | sì |
| Vista in sezione semplice | `FusionDrawingViewSimpleSectionCommand` | `Views 🧪` | sì (presente) | sì |
| Vista in sezione | `FusionDrawingViewSectionCommand` | `Views 🧪` | sì (presente) | sì |
| Vista di dettaglio | `FusionDrawingViewDetailCommand` | `Views 🧪` | sì (presente) | sì |
| Vista interrotta | `FusionBrokenViewCommand` | `Views 🧪` | sì (presente) | sì |
| Vista in sezione interruzione | `FusionDrawingBreakoutSectionViewCommand` | `Views 🧪` | sì (presente) | sì |
| Vista di ritaglio | `FusionDrawingCropViewCommand` | `Views 🧪` | sì (presente) | sì |
| Vista prospettica | `FusionDrawingViewPerspectiveCommand` | `Views 🧪` | sì (presente) | sì |
| Crea schizzo | `FusionDrawingViewSketchCommand` | `DrawingSketches.add 🧪` | sì (presente) | sì |
| Orizzontale/Verticale | `FDWGGcHorizontalVerticalCommand` | — | sì (presente) | — |
| Coincidente | `FDWGGcCoincidentCommand` | — | sì (presente) | — |
| Tangente | `FDWGGcTangentCommand` | — | sì (presente) | — |
| Uguale | `FDWGGcEqualCommand` | — | sì (presente) | — |
| Parallelo | `FDWGGcParallelCommand` | — | sì (presente) | — |
| Perpendicolare | `FDWGGcPerpendicularCommand` | — | sì (presente) | — |
| Fisso | `FDWGGcFixCommand` | — | sì (presente) | — |
| Concentrico | `FDWGGcConcentricCommand` | — | sì (presente) | — |
| Collineare | `FDWGGcCollinearCommand` | — | sì (presente) | — |
| Simmetrico | `FDWGGcSymmetricCommand` | — | sì (presente) | — |
| Offset | `FusionDrawingOffsetCommand` | — | sì (presente) | — |
| Ruota | `FusionDocRotateCmd` | — | sì (presente) | — |
| Ritaglia | `FusionDrawingTrimCommand` | — | sì (presente) | — |
| Estendi | `FusionDrawingExtendCommand` | — | sì (presente) | — |
| Sposta | `FusionDrawingMoveCmd` | — | sì (presente) | — |
| Copia | `FusionDrawingCopyCommand` | — | sì (presente) | — |
| Elimina | `FusionDrawingEraseCmd` | `Drawing.deleteEntities` | sì (presente) | no |
| Aggiorna proprietà | `DrawingsPropertyRefreshCmd` | — | sì (presente) | — |
| Linea d'asse | `FusionDrawingCenterlineCommand` | — | sì (presente) | — |
| Centro | `FusionDrawingCentermarkCommand` | — | sì (presente) | — |
| Serie centrata | `FusionDrawingCenterPatternCommand` | — | sì (presente) | — |
| Estensione spigolo | `FusionDrawingEdgeExtensionCmd` | — | sì (presente) | — |
| Quota | `FusionDrawingSingleDimensionCmd` | `DrawingDimensions 🧪` | sì (presente) | sì |
| Quota automatica | `FusionDrawingAutoDimensionCommand` | — | sì (presente) | — |
| Riordina | `FusionDrawingTidyUpCommand` | — | sì (presente) | — |
| Quota coordinata | `FusionDrawingOrdinateDimensionCmd` | — | sì (presente) | — |
| Cambia impostazioni di automazione | `FusionDocAutomationSettingsCmd` | `DocumentSettings 🧪` | sì (presente) | sì |
| Quota lineare | `FusionDrawingLinearDimensionCmd` | `DrawingDimensions.addLinearDimension 🧪` | sì (presente) | sì |
| Quota allineata | `FusionDrawingAlignedDimensionCmd` | `DrawingDimensions.addLinearDimension 🧪` | sì (presente) | sì |
| Quota angolare | `FusionDrawingAngularDimensionCmd` | `DrawingDimensions.addAngularDimension 🧪` | sì (presente) | no |
| Quota raggio | `FusionDrawingRadialDimensionCmd` | `DrawingDimensions.addRadialDimension 🧪` | sì (presente) | sì |
| Quota diametro | `FusionDrawingDiameterDimensionCmd` | `DrawingDimensions.addDiameterDimension 🧪` | sì (presente) | sì |
| Quota radiale ridotta | `FusionDrawingJoggedRadiusDimensionCmd` | `DrawingDimensions.addJoggedRadiusDimension 🧪` | sì (presente) | no |
| Quota lunghezza arco | `FusionDrawingArcDimensionCmd` | `DrawingDimensions.addArcLengthDimension 🧪` | sì (presente) | no |
| Quota max min. curva | `FusionDocMinMaxDimensionCmd` | — | sì (presente) | — |
| Quota linea di base | `FusionDrawingBaselineDimensionCmd` | — | sì (presente) | — |
| Quota in serie | `FusionDrawingChainDimensionCmd` | — | sì (presente) | — |
| Disponi quote | `FusionDrawingDimensionArrangeCmd` | — | sì (presente) | — |
| Accoppia quota | `FusionDrawingMatchDimensionCmd` | — | sì (presente) | — |
| Inverti frecce | `FusionDrawingFlipDimArrowCmd` | — | sì (presente) | — |
| Interruzione quota | `FusionDrawingDimensionBreakCmd` | — | sì (presente) | — |
| Sostituisci con aspetto configurato | `FusionDrawingReplaceDimensionWithConfigAspectCmd` | `DrawingDimensions 🧪` | configurazioni: no | sì |
| Testo | `FusionDrawingMTextCommand` | — | sì (presente) | — |
| Nota | `FusionDrawingNoteCommand` | — | sì (presente) | — |
| Nota direttrice | `FusionDrawingLeaderCommand` | — | sì (presente) | — |
| Nota su foro e filettatura | `FusionDrawingHoleThreadNoteLeaderCommand` | — | sì (presente) | — |
| Nota piega | `FusionDrawingBendNoteLeaderCommand` | — | sì (presente) | — |
| Attributo | `FusionDrawingAttDefCommand` | — | sì (presente) | — |
| Stato della superficie | `FusionDrawingSurfaceTextureCmd` | — | sì (presente) | — |
| Riquadro di controllo della geometria | `FusionDrawingFeatureControlFrameCmd` | `DrawingSymbols.addFeatureControlFrame 🧪` | sì (presente) | sì |
| Identificatore del riferimento | `FusionDrawingDatumIdCmd` | `DrawingSymbols.addDatumIdentifier 🧪` | sì (presente) | sì |
| Saldatura | `FusionDrawingWeldSymbolCmd` | — | sì (presente) | — |
| Rastremazione e inclinazione | `FusionDrawingTaperSlopeSymbolCmd` | `DrawingSymbols.addTaperSlopeSymbol 🧪` | sì (presente) | no |
| Simbolo spigolo | `FusionDrawingEdgeSymbolCmd` | `DrawingSymbols.addEdgeSymbol 🧪` | sì (presente) | no |
| Gestisci simboli di schizzo | `FusionDrawingManageSketchSymbolCmd` | — | sì (presente) | — |
| Inserisci simbolo di schizzo | `FusionDrawingInsertSketchSymbolCmd` | — | sì (presente) | — |
| Crea simbolo di schizzo | `FusionDrawingCreateSketchSymbolCmd` | — | sì (presente) | — |
| Inserisci immagine | `FusionDrawingImageInsertCommand` | `Images.insert 🧪` | sì (presente) | sì |
| Immagine | `FusionDrawingBlockEditorImageInsertCommand` | `Images.insert 🧪` | sì (presente) | sì |
| Inserisci immagine | `FusionDrawingTemplateImageInsertCommand` | `Images.insert 🧪` | sì (presente) | sì |
| Elenco parti | `FusionDrawingCreatePartsListCommand` | — | sì (presente) | — |
| Tabella | `FusionDrawingNewTableCommand` | `CustomTables.add 🧪` | sì (presente) | sì |
| Segnaposto tabella | `FusionDrawingNewTableTemplateCommand` | — | sì (presente) | — |
| Tabella personalizzata | `FusionDrawingEmptyTableCommand` | `CustomTables.add 🧪` | sì (presente) | sì |
| Elenco parti | `FusionDrawingPartsListTableCommand` | — | sì (presente) | — |
| Numero di riferimento | `FusionDrawingBalloonCommand` | — | sì (presente) | — |
| Tabella di piega | `FusionDrawingBendTableCommand` | `BendTables 🧪` | sì (presente) | no |
| Identificatore di piega | `FusionDrawingBendIDCommand` | — | sì (presente) | — |
| Tabella fori | `FusionDrawingHoleTableCommand` | `HoleTables 🧪` | sì (presente) | sì |
| Tabella di configurazione | `FusionDrawingConfigTableCommand` | — | configurazioni: no | — |
| Cronologia revisioni | `FusionDrawingRevisionTableCommand` | `RevisionTable 🧪` | sì (presente) | no |
| Contrassegno di revisione | `FusionDrawingRevMarkerCommand` | — | sì (presente) | — |
| Fumetto di revisione | `FusionDocRevCloudCommand` | — | sì (presente) | — |
| Rinumera | `FusionDrawingRenumberCommand` | — | sì (presente) | — |
| Allinea numeri di riferimento | `FusionDrawingAlignBalloonCommand` | — | sì (presente) | — |
| Preferenze di automazione | `DrawingAutomationPreferenceCmd` | `AutomationPreferences 🧪` | sì (presente) | no |
| Termina cartiglio | `FusionDrawingBlockCloseCommand` | — | sì (presente) | — |
| Termina bordo | `FusionDrawingBorderCloseCommand` | — | sì (presente) | — |
| Termina schizzo | `FusionDrawingSketchCloseCommand` | — | sì (presente) | — |
| Termina simbolo di schizzo | `FusionDrawingSketchSymbolCloseCommand` | — | sì (presente) | — |
| Termina schizzo | `FusionDrawingViewSketchCloseCommand` | — | sì (presente) | — |
| Esporta PDF | `FusionDrawingExportPDFCommand` | `DrawingExportManager.createPDFExportOptions` | sì (presente) | sì |
| Esporta DWG | `ExportFusionDrawingDocumentCommand` | `DrawingExportManager.createDWGExportOptions` | sì (presente) | sì |
| Esporta foglio come DXF | `FusionDrawingExportDXFCommand` | `DrawingExportManager.createDXFExportOptions` | sì (presente) | no |
| Modello di disegno di output | `ExportFusionDrawingTemplateCommand` | — | sì (presente) | — |
| Esporta CSV | `FusionDrawingExportPartsListCommand` | — | sì (presente) | — |
| Debug del disegno | `FusionDrawingDebugCommand` | — | sì (presente) | — |
| Riepilogo modifiche | `DrawingShowChangeAwarenessToolbarCmd` | — | sì (presente) | — |
| Misura | `FusionDrawingMeasureCommand` | — | sì (presente) | — |
| Cronologia | `FusionDocShowHistoryForDrawingToolbarCommand` | — | sì (presente) | — |

## Disegno (Drawing) / Scheda COMPONENTI ELETTRONICI (`ElectronicsTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Vista pila di layer | `ECADLayerStackDiagramCmd` | — | elettronica: skill a parte | — |
| Vista rame | `ECADCopperViewCmd` | — | elettronica: skill a parte | — |
| Vista forature | `ECADDrillViewCmd` | — | elettronica: skill a parte | — |
| Tabella Pila di layer | `LayerStackTableCmd` | — | elettronica: skill a parte | — |
| Tabella forature | `ECADDrillTableCmd` | — | elettronica: skill a parte | — |

## Disegno (Drawing) / Scheda GESTISCI (`ManageTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Aggiorna | `ManageExtRefreshCmd` | — | sì (presente) | — |

## Disegno (Drawing) / Scheda CARTIGLIO (`TitleBlockTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Linea | `FusionDrawingLineCommand` | `DrawingSketch.lines 🧪` | sì (presente) | sì |
| Rettangolo mediante 2 punti | `FusionDrawingRectangleCommand` | `DrawingSketch.rectangles 🧪` | sì (presente) | no |
| Cerchio centro-raggio | `FusionDrawingCircleCommand` | `DrawingSketch.circles 🧪` | sì (presente) | no |
| Ellisse | `FusionDrawingEllipseCommand` | `DrawingSketch.ellipses 🧪` | sì (presente) | no |
| Arco a 3 punti | `FusionDrawingArcCommand` | `DrawingSketch.arcs 🧪` | sì (presente) | sì |
| Direttrice | `FusionDrawingArrowCommand` | — | sì (presente) | — |
| Etichetta | `FusionDrawingLabelDefCommand` | — | sì (presente) | — |
| Quota dello schizzo | `FDWGSketchSmartConstarintDimCommand` | — | sì (presente) | — |

## Disegno (Drawing) / Scheda menu (File, barre fisse, tasto destro, radiale) (`Menu`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Riassocia | `FusionDrawingDimReassociateCmd` | `DrawingDimensions 🧪` | sì (presente) | sì |
| Elimina vincolo | `FusionDocDeleteConstraintCmd` | — | sì (presente) | — |
| Riassocia | `FusionDrawingSmartObjReassociateCmd` | — | sì (presente) | — |
| Riassocia | `FusionDrawingCustomLeaderReassociateCmd` | — | sì (presente) | — |
| Continua | `FusionDrawingContinueCmd` | — | sì (presente) | — |
| Annulla | `CancelCommand` | — | sì (presente) | — |
| Modifica vista | `FusionDrawingViewEditCommand` | `Views 🧪` | sì (presente) | sì |
| Annulla | `FusionDrawingUndoCommand` | — | sì (presente) | — |
| Ripeti | `FusionDrawingRedoCommand` | — | sì (presente) | — |
| Modifica impostazioni documento | `FusionChangeMultiDocSettingCommand` | — | sì (presente) | — |
| FusionChangeDocumentSettingsCommand | `FusionChangeDocumentSettingsCommand` | `Documents.add` | sì (presente) | sì |
| Modifica impostazioni documento | `FusionChangeDocSettingCommand` | `DocumentSettings 🧪` | sì (presente) | sì |
| Importa impostazioni documento | `FusionImportDocSettingsCommand` | `Documents.add` | sì (presente) | sì |
| Modifica font | `FusionChangeFontCommand` | — | sì (presente) | — |
| Modifica gruppo altezza testo | `FusionChangeTextHeightGroupCommand` | — | sì (presente) | — |
| Modifica gruppo larghezza linea | `FusionChangeLineWidthGroupCommand` | — | sì (presente) | — |
| Modifica unità di quota | `FusionChangeDimensionUnitsCommand` | `DocumentSettings 🧪` | sì (presente) | sì |
| Modifica ambito revisione | `FusionChangeRevisionScopeCommand` | — | sì (presente) | — |
| Modifica impostazioni foglio | `FusionChangeMultiSheetSettingsCommand` | — | sì (presente) | — |
| Modifica dimensioni foglio | `FusionChangeSheetSizeCommand` | `DocumentSettings 🧪` | sì (presente) | sì |
| Modifica cartiglio | `FusionChangeTitleBlockCommand` | `TitleBlocks 🧪` | sì (presente) | sì |
| Modifica visualizzazione bordo | `FusionChangeDisplayBorderCommand` | `Viewport.camera` | sì (presente) | sì |
| Modifica visualizzazione cartiglio | `FusionChangeDisplayTitleBlockCommand` | `TitleBlocks 🧪` | sì (presente) | sì |
| Apri | `OpenRelatedDesignCommand` | `Documents.add` | sì (presente) | sì |
| Reimposta | `FusionDocRestoreDefaultsCmd` | — | sì (presente) | — |
| Mostra in posizione | `ShowInLocationDrawingCmd` | — | sì (presente) | no |
| Impila quote | `FusionDrawingDimensionStackArrangeCmd` | `DrawingDimensions 🧪` | sì (presente) | sì |
| Allinea quote | `FusionDrawingDimensionAlignArrangeCmd` | `DrawingDimensions 🧪` | sì (presente) | sì |
| Accoppia quota | `FusionDrawingMatchDimCntxMenuCmd` | `DrawingDimensions 🧪` | sì (presente) | sì |
| Inverti frecce | `FusionDrawingFlipDimArrowCntxMenuCmd` | `DrawingDimensions 🧪` | sì (presente) | sì |
| Aggiungi interruzione quota | `FusionDrawingAddDimensionBreakCmd` | `DrawingDimensions 🧪` | sì (presente) | sì |
| Rimuovi interruzione quota | `FusionDrawingRemoveDimensionBreakCmd` | `DrawingDimensions 🧪` | sì (presente) | sì |
| Cambia configurazione | `SwitchConfigurationCommand` | — | configurazioni: no | — |
| Sostituisci con aspetto configurato | `FusionDrawingReplaceDimensionWithConfigAspectContextMenuCmd` | `DrawingDimensions 🧪` | configurazioni: no | sì |
| Modifica vista di ritaglio | `FusionDrawingCropViewEditCommand` | `Views 🧪` | sì (presente) | sì |
| Mostra/nascondi Contorno di ritaglio | `FusionDrawingCropOutlineCommand` | `Views 🧪` | sì (presente) | sì |
| Modifica bordo | `FusionDrawingBorderEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Mostra/Nascondi | `FusionChangeBorderVisibilityCommand` | — | sì (presente) | no |
| Nuovo cartiglio | `FusionDrawingNewTitleBlockCommand` | `TitleBlocks 🧪` | sì (presente) | sì |
| Modifica cartiglio | `FusionDrawingBlockEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica proprietà | `FusionEditPropertiesCommand` | — | sì (presente) | — |
| Ripristina proprietà | `FusionResetPropertiesCommand` | — | sì (presente) | — |
| Mostra/Nascondi | `FusionChangeTitleBlockVisibilityCommand` | `TitleBlocks 🧪` | sì (presente) | sì |
| Modifica schizzo | `FusionDrawingSketchEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Modifica schizzo | `FusionDrawingViewSketchEditCommand` | `Views 🧪` | sì (presente) | sì |
| Modifica quote automatiche | `FusionDrawingAutoDimensionEditCommand` | `DrawingDimensions 🧪` | sì (presente) | sì |
| Ottieni quota alternativa | `FusDocGetAlternateDimCommand` | — | sì (presente) | — |
| FusDocGetAlternatePointCommand | `FusDocGetAlternatePointCommand` | — | sì (presente) | — |
| Taglia | `FusionDocCutSketchCommand` | — | sì (presente) | — |
| Copia | `FusionDocCopySketchCommand` | — | sì (presente) | — |
| Incolla | `FusionDocPasteSketchCommand` | — | sì (presente) | — |
| Taglia | `FusionDocCutGeomEntityCommand` | — | sì (presente) | — |
| Copia | `FusionDocCopyGeomEntityCommand` | — | sì (presente) | — |
| Incolla | `FusionDocPasteGeomEntityCommand` | — | sì (presente) | — |
| Taglia | `FusionDocCutMtextCommand` | — | sì (presente) | — |
| Copia | `FusionDocCopyMtextCommand` | — | sì (presente) | — |
| Incolla | `FusionDocPasteTextCommand` | — | sì (presente) | — |
| Incolla | `FusionDocPasteCustomMTextCommand` | — | sì (presente) | — |
| Copia | `FusionDocCopyCustomTableCommand` | — | sì (presente) | — |
| Incolla | `FusionDocPasteCustomTableCommand` | — | sì (presente) | — |
| Incolla | `FusionDocPasteExternalCustomTableCommand` | — | sì (presente) | — |
| Elimina | `FusionDocDeleteCmd` | `Drawing.deleteEntities` | sì (presente) | no |
| Elimina | `FusionDrawingSketchDeleteCommand` | — | sì (presente) | — |
| Mostra/Nascondi | `SketchShowHideCommand` | — | sì (presente) | no |
| Mostra/Nascondi | `FusionDrawingShowHideCommand` | — | sì (presente) | no |
| FusionDrawingShowHideSketchesSketchCommand | `FusionDrawingShowHideSketchesSketchCommand` | — | sì (presente) | no |
| Mostra tutti i componenti | `FusionDrawingShowAllChildCommand` | — | sì (presente) | no |
| Mostra tutti i componenti | `FusionDrawingShowAllCommand` | — | sì (presente) | no |
| Scopri tutti i componenti | `FusionDrawingUnsuppressAllCommand` | — | sì (presente) | — |
| Cronologia progetto | `FusionDocShowHistoryForDesignCommand` | — | sì (presente) | no |
| Disegni precedenti | `FusionDocShowHistoryForDrawingCommand` | — | sì (presente) | no |
| Modifica proprietà modello | `FusionDocModelPropertyEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |
| Sopprimi | `FusionDrawingSuppressCommand` | — | sì (presente) | — |
| Scopri | `FusionDrawingUnsuppressCommand` | — | sì (presente) | — |
| Scopri tutti i componenti | `FusionDrawingUnsuppressAllChildCommand` | — | sì (presente) | — |
| Sopprimi tutto eccetto i selezionati | `FusionDrawingSuppressAllExceptSelectedCommand` | `Selections` | sì (presente) | no |
| Aggiorna | `FusionDrawingUpdateLinkTable` | — | sì (presente) | — |
| Interrompi | `FusionDrawingBreakLinkTable` | — | sì (presente) | — |
| Modifica vista in sezione interruzione | `FusionDrawingBreakoutSectionViewEditCommand` | `Views 🧪` | sì (presente) | sì |

## Rendering / Scheda RENDERING (`RenderTab`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Visualizzazione AI | `AIVisualizationCommand` | — | consuma token: no senza richiesta | — |
| Impostazioni scena | `RenderingEnvCmd` | `RenderManager.sceneSettings` | sì (presente) | sì |
| Luce | `LightCommand` | `Lights 🧪` | sì (presente) | no |
| Controlli della mappa di texture | `TextureMappingCommand` | `TextureMapControl` | sì (presente) | no |
| Controllo priorità dielettrica | `DielectricPriorityControlCmd` | — | sì (presente) | — |
| Rendering su area graf. | `InCanvasRenderCommand` | `RenderManager.inCanvasRendering` | sì (presente) | no |
| Impostazioni di rendering su area grafica | `InCanvasRenderSettingsCommand` | `RenderManager.inCanvasRendering` | sì (presente) | no |
| Cattura immagine... | `SaveAsImageCommand` | `Viewport.saveAsImageFile` | sì (presente) | sì |
| Rendering | `A360RenderCommand` | `RenderManager.rendering` | sì (presente) | sì |

## Rendering / Scheda menu (File, barre fisse, tasto destro, radiale) (`Menu`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Sopprimi | `SuppressNamedLightCmd` | `Light.isSuppressed 🧪` | sì (presente) | sì |
| Sopprimi tutto | `SuppressAllNamedLightsCmd` | `Light.isSuppressed 🧪` | sì (presente) | sì |
| Scopri | `UnsuppressNamedLightCmd` | `Light.isSuppressed 🧪` | sì (presente) | sì |
| Scopri tutto | `UnsuppressAllNamedLightsCmd` | `Light.isSuppressed 🧪` | sì (presente) | sì |

## Animazione / Scheda ANIMAZIONE (`Animation`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Nuovo storyboard | `PublisherCreateStoryboardCommand` | `Storyboards.add` | sì (presente) | sì |
| Trasforma componenti | `PublisherMoveComponentsCommand` | — | sì (presente) | — |
| Ripristina posizione iniziale | `PublisherRestoreHomeCommand` | — | sì (presente) | — |
| Esplosione automatica: un livello | `PublisherExplodeDirectChildrenCommand` | — | sì (presente) | — |
| Esplosione automatica: tutti i livelli | `PublisherExplodeAllPartsCommand` | — | sì (presente) | — |
| Esplosione manuale | `PublisherManualExplodeCommand` | — | sì (presente) | — |
| Mostra/Nascondi | `PublisherVisibilityToggleCmd` | — | sì (presente) | — |
| Aspetto | `PublisherAppearanceCommand` | `Appearances` | sì (presente) | sì |
| Visualizza | `PublisherToggleCameraRecordingCmd` | `Storyboard.isViewRecordingOn` | sì (presente) | no |
| Pubblica video | `ExportVideoCommand` | — | sì (presente) | — |

## Animazione / Scheda menu (File, barre fisse, tasto destro, radiale) (`Menu`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| PublisherEditStoryboardCmd | `PublisherEditStoryboardCmd` | `Storyboards` | sì (presente) | sì |
| Inverti | `ReverseSequenceEntryCmd` | — | sì (presente) | — |
| Copia | `PublisherCopyCommand` | — | sì (presente) | — |
| Incolla | `PublisherPasteCommand` | — | sì (presente) | — |
| Durata | `PublisherDurationCmd` | — | sì (presente) | — |
| Modifica inizio/fine | `PublisherEditActionCmd` | — | sì (presente) | — |
| Modifica azione | `PublisherEditTransformActionCommand` | — | sì (presente) | — |
| Modifica inizio | `PublisherEditSmartObjectActionCmd` | — | sì (presente) | — |
| Elimina | `PublisherDeleteCommand` | — | sì (presente) | — |
| Crea richiamo | `CalloutCommand` | — | sì (presente) | — |
| Attiva/disattiva materiale | `PublisherMaterialToggleCommand` | — | sì (presente) | no |
| Modifica ambito materiale | `PublisherScopeMaterialCommand` | — | sì (presente) | — |
| Mostra/nascondi linee finali | `PublisherTrailVisibilityCommand` | — | sì (presente) | no |
| Mostra tutte le linee finali | `PublisherTrailShowAllCommand` | — | sì (presente) | no |
| Nascondi tutte le linee finali | `PublisherTrailHideAllCommand` | — | sì (presente) | no |
| PublisherUpdateCmd | `PublisherUpdateCmd` | — | sì (presente) | — |
| Crea gruppo di selezione | `PublisherCreateSelectionGroupCmd` | `Selections` | sì (presente) | no |
| Isola | `PublisherIsolateCmd` | — | sì (presente) | no |
| Annulla isolamento | `PublisherUnisolateCmd` | — | sì (presente) | — |
| Rinomina | `RenameStoryboardShellCmd` | — | sì (presente) | — |
| Allinea ora di inizio | `AlignActionStartTimesCmd` | — | sì (presente) | — |
| Allinea ora di fine | `AlignActionEndTimesCmd` | — | sì (presente) | — |
| Seleziona tutti dopo | `SelectAllAfterCmd` | `Selections` | sì (presente) | no |
| Seleziona tutti prima | `SelectAllBeforeCmd` | `Selections` | sì (presente) | no |
| Espandi | `PublisherExpandCompositeActionsCmd` | — | sì (presente) | — |
| Elimina azioni | `PublisherDeleteActorCommand` | — | sì (presente) | — |
| Trova nel browser | `PublisherFindInBrowser` | — | sì (presente) | — |
| Trova nella finestra | `PublisherFindInWindow` | — | nesting: estensione a pagamento — da verificare | — |
| Modifica richiamo | `CalloutEditCommand` | `TimelineObject.rollTo` | sì (presente) | sì |

## Comuni (menu File e barre fisse) / Scheda menu (File, barre fisse, tasto destro, radiale) (`Menu`)

| Comando | Identificativo | API | Personal | Provato |
|---|---|---|---|---|
| Mostra comandi di testo | `ShowTextCommandsCommand` | — | sì (presente) | no |
| Mostra Home | `ShowFusionHomeCmd` | — | sì (presente) | no |
| Nascondi pannello dati | `DashboardModeSwitchCommand` | — | sì (presente) | — |
| File | `FileSubMenuCommand` | `Documents.add` | sì (presente) | sì |
| Nuovo... | `NewDocumentCommand` | `Documents.add` | sì (presente) | sì |
| Nuovo disegno | `NewDrawingMenuCommand` | `Documents.add` | sì (presente) | sì |
| Dal progetto | `NewFusionDrawingDocumentCommand` | `Documents.add` | sì (presente) | sì |
| Dal progetto | `ECADNewDrawingDocumentCommand` | `Documents.add` | sì (presente) | sì |
| Dal progetto | `ECADNewDrawingFromPCB3dCommand` | `Documents.add` | sì (presente) | sì |
| Da animazione | `PublisherNewDrawingDocumentCommand` | `Documents.add` | sì (presente) | sì |
| Nuovo modello di disegno | `NewFusionDrawingTemplateCommand` | `Documents.add` | sì (presente) | sì |
| Apri... | `OpenCommand` | `Documents.add` | sì (presente) | sì |
| Documenti recuperati aperti (0) | `NotifyAutoSaveFilesCommand` | `Documents.add` | sì (presente) | sì |
| Carica... | `UploadCommand` | `Documents.add` | sì (presente) | sì |
| Salva | `PLM360SaveCommand` | `Documents.add` | sì (presente) | sì |
| Salva con nome | `PLM360SaveAsCommand` | `Documents.add` | sì (presente) | sì |
| Salva come più recente | `PLM360SaveAsLatestOnQATCommand` | `Documents.add` | sì (presente) | sì |
| Salva stato calcolato | `SaveComputedStateCommand` | `Documents.add` | sì (presente) | sì |
| Esporta... | `ExportCommand` | `Documents.add` | sì (presente) | sì |
| Crea versione | `CreateVersionCommand` | `Document.save` | sì (presente) | sì |
| Stampa... | `FusionDrawingPrintCommand` | `Documents.add` | sì (presente) | sì |
| Condividi collegamento file | `SimpleSharingPublicLinkCommand` | — | sì (presente) | — |
| Visualizza dettagli sul Web | `PLM360OpenDetailsCommand` | `Documents.add` | sì (presente) | sì |
| Visualizza | `ViewWidgetCommand` | `Viewport.camera` | sì (presente) | sì |
| Nascondi ViewCube | `HideViewCubeCommand` | `Viewport.camera` | sì (presente) | sì |
| Mostra ViewCube | `ShowViewCubeCommand` | `Viewport.camera` | sì (presente) | sì |
| Nascondi browser | `HideBrowserCommand` | — | sì (presente) | no |
| Mostra browser | `ShowBrowserCommand` | — | sì (presente) | no |
| Nascondi commenti | `HideActivityFeedCommand` | — | sì (presente) | no |
| Mostra commenti | `ShowActivityFeedCommand` | — | sì (presente) | no |
| Nascondi tavolozza comandi | `HideCommandPaletteCommand` | — | sì (presente) | no |
| Mostra tavolozza dei comandi | `ShowCommandPaletteCommand` | — | sì (presente) | no |
| Nascondi comandi di testo | `HideTextCommandsCommand` | — | sì (presente) | no |
| Nascondi barra di navigazione | `HideNavigationToolbarCommand` | — | sì (presente) | no |
| Mostra barra di navigazione | `ShowNavigationToolbarCommand` | — | sì (presente) | no |
| Nascondi barra degli strumenti dei comandi | `HideCommandToolbarCommand` | — | sì (presente) | no |
| Mostra barra degli strumenti dei comandi | `ShowCommandToolbarCommand` | — | sì (presente) | no |
| Mostra pannello dati | `DashboardModeOpenCommand` | `Documents.add` | sì (presente) | sì |
| Nascondi pannello dati | `DashboardModeCloseCommand` | `Documents.add` | sì (presente) | sì |
| Nascondi sovrapposizione prestazioni | `HidePerformanceOverlayCommand` | — | sì (presente) | no |
| Mostra sovrapposizione prestazioni | `ShowPerformanceOverlayCommand` | — | sì (presente) | no |
| Ripristina layout di default | `ResetToDefaultLayoutCommand` | — | sì (presente) | — |
| Apri... | `OpenDocumentCommand` | `Documents.add` | sì (presente) | sì |
| Salva localmente | `SaveDocumentCommand` | `Documents.add` | sì (presente) | sì |
| Annulla più volte | `UndoDropDown` | — | sì (presente) | — |
| Annulla | `DoraUndoCommand` | — | sì (presente) | — |
| Ripeti più volte | `RedoDropDown` | — | sì (presente) | — |
| Ripeti | `DoraRedoCommand` | — | sì (presente) | — |
| Mostra NTest | `NTestExcMetaCommand` | — | sì (presente) | — |
| Consapevolezza modifiche utente | `ShowChangeAwarenessQATCmd` | — | sì (presente) | no |
| Orbita | `OrbitCommand` | `Viewport.camera` | sì (presente) | sì |
| Ingrandisci finestra | `ZoomFitCommandGroup` | `Viewport.camera` | nesting: estensione a pagamento — da verificare | sì |
| Impostazioni di visualizzazione | `ViewDisplayCommand` | `Viewport.camera` | sì (presente) | sì |
| Stile di visualizzazione | `ViewVisualStyleCommand` | `Viewport.camera` | sì (presente) | sì |
| Ambiente | `ViewEnvCommand` | `Viewport.camera` | sì (presente) | sì |
| Preset grafica | `ViewGraphicsPresetCommand` | `Viewport.camera` | sì (presente) | sì |
| Effetti | `ViewEffectCommand` | `Viewport.camera` | sì (presente) | sì |
| Visibilità oggetto | `VisibilityOverrideCommand` | — | sì (presente) | no |
| Inquadratura | `ViewCameraCommand` | `Viewport.camera` | sì (presente) | sì |
| Stile di visualizzazione | `SplitViewVisualStyleCommand` | `Viewport.camera` | sì (presente) | sì |
| Inquadratura | `SplitViewCameraCommand` | `Viewport.camera` | sì (presente) | sì |
| Offset del piano di base | `GroundPlaneOffsetCommand` | `Design.setGroundPlaneOffset` | sì (presente) | no |
| Attiva modalità schermo intero | `ShowWorkspaceFullScreenCommand` | — | sì (presente) | no |
| Esci dalla modalità schermo intero | `ShowWorkspaceNormalCommand` | — | sì (presente) | no |
| Griglia e snap | `ViewLayoutGridCommand` | `Viewport.camera` | sì (presente) | sì |
| Impostazioni griglia | `DefineGridCmd` | `Viewport.camera` | sì (presente) | sì |
| Spostamento incrementale | `ToggleIncrementalMoveCmd` | — | sì (presente) | no |
| Imposta incrementi | `SetSnapValueCmd` | `Viewport.camera` | sì (presente) | sì |
| Finestre | `SplitViewWindowSyncCommand` | `Viewport.camera` | nesting: estensione a pagamento — da verificare | sì |
| Vista singola | `SingleViewCmd` | `Viewport.camera` | sì (presente) | sì |
| Viste multiple | `MultiViewCmd` | `Viewport.camera` | sì (presente) | sì |
| Reimposta viste | `SplitViewResetCmd` | `Viewport.camera` | sì (presente) | sì |
| Accesso di base | `BasicAccessCommand` | — | sì (presente) | — |
| 0 E - 0 W | `HealthStatusCommand` | — | sì (presente) | — |
| Scaduto: abbonati subito | `TryToBuyCommand` | — | sì (presente) | — |
| Aggiorna ad un abbonamento a Fusion | `RequestTrialCommand` | — | sì (presente) | — |
| ConnectivityStatusCommand | `ConnectivityStatusCommand` | — | sì (presente) | — |
| Manutenzione del servizio cloud. | `CloudServiceStatusCommand` | — | sì (presente) | — |
| UpdateAvailableCommand | `UpdateAvailableCommand` | — | sì (presente) | — |
| NotificationCommand | `NotificationCommand` | — | sì (presente) | — |
| Autodesk Assistant | `AANewChatCommand` | `Documents.add` | sì (presente) | sì |
| FeaturePacksCommand | `FeaturePacksCommand` | — | sì (presente) | — |
| CloudStatusCommand | `CloudStatusCommand` | — | sì (presente) | — |
| Centro notifiche | `NotificationCenterCommand` | — | sì (presente) | — |
| Subscription | `SubscriptionCommand` | — | sì (presente) | — |
| Guida | `HelpGroupCommand` | — | sì (presente) | — |
| Apprendimento e documentazione | `LearningAndHelpCommand` | — | sì (presente) | — |
| Apprendimento personalizzato | `HelpCommand` | — | sì (presente) | — |
| Documentazione del prodotto | `LearningAndTutorialsCommand` | — | sì (presente) | — |
| Impostazione rapida | `LearningPaletteCommand` | — | sì (presente) | — |
| Autodesk Assistant | `AAChatCommand` | — | sì (presente) | — |
| Comunità | `CommunityCommand` | — | sì (presente) | — |
| Forum | `ForumCommand` | — | sì (presente) | — |
| Programma Insider | `SubmitAnIdeaCommand` | — | sì (presente) | — |
| Blog | `BlogCommand` | — | sì (presente) | — |
| Supporto e diagnostica | `SupportAndDiagnosticsCommand` | — | sì (presente) | — |
| Ottieni supporto | `FeedbackCommand` | — | sì (presente) | — |
| Annota file di registro | `AnnotateLogFileCommand` | `Documents.add` | sì (presente) | sì |
| File di registro di diagnostica | `GatherDiagnosticsDataCommand` | — | sì (presente) | — |
| Diagnostica grafica | `GraphicsDiagnosticsCommand` | — | sì (presente) | — |
| Cancella dati cache | `ClearUserCacheCommand` | — | sì (presente) | — |
| Service Utility | `ServiceUtilityCommand` | — | sì (presente) | — |
| Segnala problemi di prestazioni | `PerfFeedbackRecorderCmd` | — | sì (presente) | — |
| Entra in contatto con un esperto | `StreetTeamCommand` | — | sì (presente) | — |
| Invia feedback | `PreReleaseFeedbackCommand` | — | distinta e rilasci (Manage): no | — |
| Segnala un problema | `ReportProblemCmd` | — | sì (presente) | — |
| Verifica aggiornamenti | `UpdateNowCommand` | — | sì (presente) | — |
| Novità | `WhatsNewCommand` | `Documents.add` | sì (presente) | sì |
| Note di rilascio | `ReleaseNotesCommand` | — | distinta e rilasci (Manage): no | — |
| Informazioni | `AboutBoxCommand` | — | sì (presente) | — |
| Esercitazioni | `TutorialsCommand` | — | sì (presente) | — |
| Riferimento rapido | `QuickStartCommand` | — | sì (presente) | — |
| Video sulle caratteristiche essenziali | `VideosCommand` | — | sì (presente) | — |
| CIPCommand | `CIPCommand` | — | sì (presente) | — |
| Nessun utente ha eseguito il login | `UserDisplayNameCommand` | `Viewport.camera` | sì (presente) | sì |
| Autodesk Account | `GoToMyAccountCommand` | — | sì (presente) | — |
| Preferenze | `PreferencesCommand` | `Preferences` | sì (presente) | no |
| Scelte rapide dei comandi | `CommandShortcutsManagerCommand` | — | sì (presente) | — |
| Cambia team | `UserHubsCommand` | — | sì (presente) | — |
| Profilo personale | `GoToMyProfileCommand` | — | sì (presente) | — |
| Cloud personale | `MyCloudCommand` | — | sì (presente) | — |
| Condividi commenti | `ShareFeedbackCommand` | — | sì (presente) | — |
| Abbonati subito | `SubscribeNowCommand` | — | sì (presente) | — |
| Esci | `QontextLogoutCommand` | — | sì (presente) | — |
| Avviso | `AlertCommand` | — | sì (presente) | — |
| CommentiPerf | `PerformanceFeedbackCommand` | — | sì (presente) | — |
| Autodesk Assistant | `ChatCommand` | — | sì (presente) | — |
| ActiveDocumentAction | `ActiveDocumentAction` | `Documents.add` | sì (presente) | sì |
