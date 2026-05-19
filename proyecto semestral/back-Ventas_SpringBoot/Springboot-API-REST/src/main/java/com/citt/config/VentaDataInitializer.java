package com.citt.config;

import com.citt.persistence.entity.Venta;
import com.citt.persistence.repository.VentaRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.List;

@Component
public class VentaDataInitializer implements CommandLineRunner {

    private final VentaRepository ventaRepository;

    public VentaDataInitializer(VentaRepository ventaRepository) {
        this.ventaRepository = ventaRepository;
    }

    @Override
    public void run(String... args) {
        if (ventaRepository.count() > 0) {
            return;
        }

        ventaRepository.saveAll(List.of(
                Venta.builder()
                        .direccionCompra("P Sherman Calle Wallabi 42 Syndey")
                        .valorCompra(22990)
                        .fechaCompra(LocalDate.of(2024, 2, 2))
                        .despachoGenerado(false)
                        .build(),
                Venta.builder()
                        .direccionCompra("Avenida siempre viva 69")
                        .valorCompra(12590)
                        .fechaCompra(LocalDate.of(2024, 3, 5))
                        .despachoGenerado(false)
                        .build(),
                Venta.builder()
                        .direccionCompra("Avenida Por atrás 1313")
                        .valorCompra(13990)
                        .fechaCompra(LocalDate.of(2024, 4, 20))
                        .despachoGenerado(false)
                        .build(),
                Venta.builder()
                        .direccionCompra("Calle presidente kirby 8528")
                        .valorCompra(9990)
                        .fechaCompra(LocalDate.of(2024, 4, 15))
                        .despachoGenerado(false)
                        .build()
        ));
    }
}
