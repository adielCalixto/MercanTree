<template>
    <div class="grid gap-4 grid-rows-2 grid-cols-1">
        <div class="stats stats-vertical shadow lg:stats-horizontal">    
            <div class="stat place-items-center">
                <div class="stat-title">Vendas</div>
                <div class="stat-value">$31,485</div>
                <div class="stat-desc">Desse mês</div>
            </div>
            
            <div class="stat place-items-start relative">
                <div class="stat-title">Últimas compras</div>

                <div class="stat-value mr-4">Lista de Compras</div>

                <a href="" class="btn btn-sm absolute  text-neutral-content right-4 top-4">Ver Tudo</a>

                <div class="overflow-x-auto place-self-center w-full mt-4">
                    <table class="table table-compact w-full">
                        <thead>
                            <tr>
                                <th></th> 
                                <th>Valor</th> 
                                <th>Cadastrante</th> 
                                <th>Data</th> 
                                <th>Status</th>
                                <th>Link</th>
                            </tr>
                        </thead> 
                        <tbody>
                            <tr>
                                <td></td>
                                <td>R$560.00</td>
                                <td>Adiel</td>
                                <td>25-04-2022</td>
                                <td>Pago</td>
                                <td><a class="link">Link</a></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>   
        </div>

        <div class="stats stats-vertical lg:stats-horizontal">  
            <div class="stat place-items-center">
                <div class="stat-title">Vendas do Dia</div>
                <div class="stat-value">31K</div>
                <div class="stat-desc">1° Jan</div>
            </div>
            
            <div class="stat place-items-center">
                <div class="stat-title">Vendas da Semana</div>
                <div class="stat-value">4,200</div>
                <div class="stat-desc">↗︎ 400 (22%)</div>
            </div>
            
            <div class="stat place-items-center">
                <div class="stat-title">Venda do Semestre</div>
                <div class="stat-value">1,200</div>
                <div class="stat-desc">↘︎ 90 (14%)</div>
            </div>        
        </div>
    </div>
</template>

<script lang="ts">
export default {
    name: 'HomeStats'
}
</script>

<style>

</style>