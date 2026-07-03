-- CreateTable
CREATE TABLE "Produtor" (
    "id" TEXT NOT NULL,
    "cpf" TEXT NOT NULL,
    "nome" TEXT NOT NULL,
    "cpf_regular" BOOLEAN NOT NULL DEFAULT true,
    "score_credito" INTEGER NOT NULL,
    "solicitacoes_recusadas" INTEGER NOT NULL DEFAULT 0,
    "historico_restricoes" INTEGER NOT NULL DEFAULT 0,
    "criado_em" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Produtor_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Propriedade" (
    "id" TEXT NOT NULL,
    "car_codigo" TEXT NOT NULL,
    "car_regular" BOOLEAN NOT NULL DEFAULT true,
    "divergencia_area_car" INTEGER NOT NULL DEFAULT 0,
    "indice_inadimplencia_regiao" DOUBLE PRECISION NOT NULL DEFAULT 0.0,

    CONSTRAINT "Propriedade_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Proposta" (
    "id" TEXT NOT NULL,
    "valor_solicitado" DOUBLE PRECISION NOT NULL,
    "operacoes_ativas_valor" DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    "status_analise" TEXT NOT NULL,
    "tecnica_bloqueio" TEXT NOT NULL,
    "justificativas" TEXT[],
    "criada_em" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "produtor_id" TEXT NOT NULL,
    "propriedade_id" TEXT NOT NULL,

    CONSTRAINT "Proposta_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Produtor_cpf_key" ON "Produtor"("cpf");

-- CreateIndex
CREATE UNIQUE INDEX "Propriedade_car_codigo_key" ON "Propriedade"("car_codigo");

-- AddForeignKey
ALTER TABLE "Proposta" ADD CONSTRAINT "Proposta_produtor_id_fkey" FOREIGN KEY ("produtor_id") REFERENCES "Produtor"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Proposta" ADD CONSTRAINT "Proposta_propriedade_id_fkey" FOREIGN KEY ("propriedade_id") REFERENCES "Propriedade"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
